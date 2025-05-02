from .repository import ScenarioRepository, TemplateRepository
from .entity import PhishingScenario, PhishingTemplate


class ScenarioService:
    @staticmethod
    def get_scenarios() -> list[PhishingScenario]:
        return ScenarioRepository.get_scenarios()

    @staticmethod
    def create_scenario(name: str, description: str, template_id: int, resource_id: int = None, domain_id: int = None) -> PhishingScenario:
        """
        Create and store a phishing scenario
        
        Args:
            name: name of the scenario
            description: description of the scenario
            template_id: ID of the email template to use
            resource_id: optional ID of the landing page resource
            domain_id: optional ID of the domain to use
            
        Returns:
            Scenario entity
        """
        return ScenarioRepository.create_scenario(name, description, template_id, resource_id, domain_id)

    @staticmethod
    def get_scenario_by_id(scenario_id: int) -> PhishingScenario:
        """
        Get a scenario by its id
        Raises
            ValueError if the scenario is not found
        """
        scenario = ScenarioRepository.get_scenario(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario with id {scenario_id} not found")
        return scenario

    @staticmethod
    def get_template_for_scenario(scenario_id: int):
        """
        Get the email template associated with a scenario
        
        Args:
            scenario_id: ID of the scenario
            
        Returns:
            Template entity
        Raises
            TemplateDoesntExist if the template is not found
        """
        return TemplateRepository.get_template_by_scenario_id(scenario_id)

class TemplateService:
    @staticmethod
    def get_templates() -> list[PhishingTemplate]:
        return TemplateRepository.get_templates()
    
    @staticmethod
    def create_template(subject: str, content: str, scenario_id: int) -> PhishingTemplate:
        return TemplateRepository.create_template(subject, content, scenario_id)
    
    @staticmethod
    def get_template_by_id(template_id: int) -> PhishingTemplate:
        return TemplateRepository.get_template_by_id(template_id)
    
    @staticmethod
    def update_template(template_id: int, subject: str, content: str) -> PhishingTemplate:
        return TemplateRepository.update_template(template_id, subject, content)
    
    @staticmethod
    def delete_template(template_id: int) -> bool:
        return TemplateRepository.delete_template(template_id)

