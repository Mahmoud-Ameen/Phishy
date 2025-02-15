from .models import TemplateModel
from .entity import PhishingTemplate
from ...extensions import db


class TemplateRepository:
    @staticmethod
    def get_templates() -> list[PhishingTemplate]:
        """ Get all phishing templates """
        templates: list[PhishingTemplate] =\
            [TemplateRepository._model_to_entity(t) for t in TemplateModel.query.all()]
        return templates

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

        template = TemplateModel(
            level=level,
            subject=subject,
            content=content
        )
        db.session.add(template)
        db.session.commit()
        return TemplateRepository._model_to_entity(template)

    @staticmethod
    def get_template_by_id(template_id: int) -> PhishingTemplate:
        template = TemplateModel.query.get(template_id)
        return TemplateRepository._model_to_entity(template)

    @staticmethod
    def _model_to_entity(template: TemplateModel) -> PhishingTemplate:
        return PhishingTemplate(
            id=template.id,
            level=template.level,
            subject=template.subject,
            content=template.content
        )
