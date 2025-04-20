from .models import TemplateModel, ScenarioModel
from .entity import PhishingTemplate, PhishingScenario
from ...core.exceptions import TemplateDoesntExist, ScenarioDoesntExist
from ...extensions import db
from typing import List, cast
from sqlalchemy.orm import RelationshipProperty


class TemplateRepository:
    @staticmethod
    def get_templates() -> list[PhishingTemplate]:
        """ Get all phishing templates """
        templates: list[PhishingTemplate] =\
            [TemplateRepository.model_to_entity(t) for t in TemplateModel.query.all()]
        return templates

    @staticmethod
    def create_template(subject: str, content: str, scenario_id: int) -> PhishingTemplate:
        """
        Create and stores a phishing template 
        
        Args:
            subject: email subject
            content: email content 
            scenario_id: ID of the scenario this template belongs to
            
        Returns:
            PhishingTemplate entity
        Raises:
            ScenarioDoesntExist: if scenario_id doesn't exist
        """
        # Verify scenario exists
        scenario = ScenarioModel.query.get(scenario_id)
        if not scenario:
            raise ScenarioDoesntExist(f"Scenario with id {scenario_id} not found")

        template = TemplateModel(
            scenario_id=scenario_id,
            subject=subject,
            content=content
        )
        db.session.add(template)
        db.session.commit()
        return TemplateRepository.model_to_entity(template)

    @staticmethod
    def get_template_by_id(template_id: int) -> PhishingTemplate:
        """
        Get a phishing template by its id
        :param template_id: template id
        :raises: TemplateDoesntExist if the template is not found
        """ ""

        try:
            template = TemplateModel.query.get(template_id)
            return TemplateRepository.model_to_entity(template)
        except AttributeError:
            raise TemplateDoesntExist(f"Template with id {template_id} not found")

    @staticmethod
    def update_template(template_id: int, subject: str, content: str) -> PhishingTemplate:
    
        template = TemplateModel.query.get(template_id)
   
        if template is None:
            raise TemplateDoesntExist(f"Template with id {template_id} not found")
        
        template.subject = subject
        template.content = content
        db.session.commit()
        return TemplateRepository.model_to_entity(template)
            

    @staticmethod
    def model_to_entity(template: TemplateModel) -> PhishingTemplate:
        return PhishingTemplate(
            id=template.id,
            subject=template.subject,
            content=template.content,
            scenario_id=template.scenario_id
        )


class ScenarioRepository:
    @staticmethod
    def create_scenario(name: str, level: int, description: str | None = None) -> PhishingScenario:
        scenario = ScenarioModel(name=name, description=description, level=level)
        db.session.add(scenario)
        db.session.commit()
        return ScenarioRepository._model_to_entity(scenario)

    @staticmethod
    def get_scenarios() -> List[PhishingScenario]:
        scenarios = ScenarioModel.query.all()
        return [ScenarioRepository._model_to_entity(scenario) for scenario in scenarios]

    @staticmethod
    def get_scenario(scenario_id) -> PhishingScenario:
        scenario = ScenarioModel.query.get(scenario_id)
        if not scenario:
            raise ScenarioDoesntExist(f"Scenario with id {scenario_id} not found")
        return ScenarioRepository._model_to_entity(scenario)

    @staticmethod
    def update_scenario(scenario_id: int, name: str, level: int, description: str | None = None) -> PhishingScenario:
        """
        Update a scenario's details
        
        Args:
            scenario_id: ID of the scenario to update
            name: New name for the scenario
            level: New difficulty level
            description: New description (optional)
            
        Returns:
            Updated PhishingScenario entity
            
        Raises:
            ScenarioDoesntExist: if scenario_id doesn't exist
        """
        scenario = ScenarioModel.query.get(scenario_id)
        if not scenario:
            raise ScenarioDoesntExist(f"Scenario with id {scenario_id} not found")

        scenario.name = name
        scenario.level = level
        scenario.description = description

        db.session.commit()
        return ScenarioRepository._model_to_entity(scenario)

    @staticmethod
    def delete_scenario(scenario_id: int) -> bool:
        """
        Delete a scenario and its associated template
        
        Args:
            scenario_id: ID of the scenario to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ScenarioDoesntExist: if scenario_id doesn't exist
        """
        scenario = ScenarioModel.query.get(scenario_id)
        if not scenario:
            raise ScenarioDoesntExist(f"Scenario with id {scenario_id} not found")

        # Delete associated template if it exists
        if scenario.template:
            db.session.delete(scenario.template)

        db.session.delete(scenario)
        db.session.commit()
        return True

    @staticmethod
    def _model_to_entity(scenario: ScenarioModel) -> PhishingScenario:
        template: PhishingTemplate | None = None
        if scenario.template is not None:
            template_model = cast(TemplateModel, scenario.template)
            template = TemplateRepository.model_to_entity(template_model)

        return PhishingScenario(
            id=scenario.id,
            name=scenario.name,
            description=scenario.description,
            level=scenario.level,
            template=template
        )
