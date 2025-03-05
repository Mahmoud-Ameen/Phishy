from .models import TemplateModel, ScenarioModel, DomainModel
from .entity import PhishingTemplate, PhishingScenario, PhishingDomain
from ...core.exceptions import DomainAlreadyExists, TemplateDoesntExist, ScenarioDoesntExist
from ...extensions import db
from typing import List
from sqlalchemy.exc import IntegrityError

class TemplateRepository:
    @staticmethod
    def get_templates() -> list[PhishingTemplate]:
        """ Get all phishing templates """
        templates: list[PhishingTemplate] =\
            [TemplateRepository._model_to_entity(t) for t in TemplateModel.query.all()]
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
        return TemplateRepository._model_to_entity(template)

    @staticmethod
    def get_template_by_id(template_id: int) -> PhishingTemplate:
        """
        Get a phishing template by its id
        :param template_id: template id
        :raises: TemplateDoesntExist if the template is not found
        """
        try:
            template = TemplateModel.query.get(template_id)
            return TemplateRepository._model_to_entity(template)
        except AttributeError:
            raise TemplateDoesntExist(f"Template with id {template_id} not found")

    @staticmethod
    def _model_to_entity(template: TemplateModel) -> PhishingTemplate:
        return PhishingTemplate(
            id=template.id,
            scenario_id=template.scenario_id,
            subject=template.subject,
            content=template.content
        )


class ScenarioRepository:
    @staticmethod
    def create_scenario(name: str, level: int, description: str | None = None) -> PhishingScenario:
        scenario = ScenarioModel(name=name, level=level, description=description)
        db.session.add(scenario)
        db.session.commit()
        return PhishingScenario(
            id=scenario.id,
            name=scenario.name,
            description=scenario.description,
            level=scenario.level
        )

    @staticmethod
    def get_scenarios() -> List[PhishingScenario]:
        return [PhishingScenario(
            id=scenario.id,
            name=scenario.name,
            description=scenario.description,
            level=scenario.level
        ) for scenario in ScenarioModel.query.all()]


class DomainRepository:
    @staticmethod
    def add_domain(domain_name: str, is_active: bool = True) -> PhishingDomain:
        try:
            domain = DomainModel(domain_name=domain_name, is_active=is_active)
            db.session.add(domain)
            db.session.commit()
            return PhishingDomain(
                domain_name=domain.domain_name,
                is_active=domain.is_active
            )
        except IntegrityError:
            raise DomainAlreadyExists(f"Domain with name {domain_name} already exists")

    @staticmethod
    def get_domains() -> List[PhishingDomain]:
        return [PhishingDomain(
            domain_name=domain.domain_name,
            is_active=domain.is_active
        ) for domain in DomainModel.query.all()]
