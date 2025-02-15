from .repository import TemplateRepository
from .entity import PhishingTemplate


class TemplateService:
    @staticmethod
    def get_templates() -> list[PhishingTemplate]:
        return TemplateRepository.get_templates()

    @staticmethod
    def create_template(subject: str, content: str, level: int) -> PhishingTemplate:
        """
        Create and stores a phishing template 
        
        Args:
            subject: email subject
            content: email content
            level: difficulty level (1-5)
            
        Returns:
            PhishingTemplate entity
        """
        return TemplateRepository.create_template(subject, content, level)

    @staticmethod
    def get_template_by_id(template_id: int) -> PhishingTemplate:
        return TemplateRepository.get_template_by_id(template_id)
