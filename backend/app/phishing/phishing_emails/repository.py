from datetime import datetime
import uuid
from .models import PhishingEmailModel
from .entity import PhishingEmail
from ... import db


class PhishingEmailRepository:
    @staticmethod
    def get_by_id(id: int) -> PhishingEmail | None:
        model = PhishingEmailModel.query.get(id)
        return PhishingEmailRepository._model_to_entity(model) if model else None

    @staticmethod
    def get_by_tracking_uuid(tracking_uuid: str) -> PhishingEmail | None:
        """Finds a PhishingEmail record by its tracking UUID."""
        model = PhishingEmailModel.query.filter_by(tracking_uuid=tracking_uuid).first()
        return PhishingEmailRepository._model_to_entity(model) if model else None

    @staticmethod
    def get_by_recipient_email(recipient_email: str) -> list[PhishingEmail]:
        emails = PhishingEmailModel.query.filter_by(recipient_email=recipient_email).all()
        return [PhishingEmailRepository._model_to_entity(email) for email in emails]

    @staticmethod
    def get_by_campaign_id(campaign_id: int) -> list[PhishingEmail]:
        emails = PhishingEmailModel.query.filter_by(campaign_id=campaign_id).all()
        return [PhishingEmailRepository._model_to_entity(email) for email in emails]

    @staticmethod
    def get_all() -> list[PhishingEmail]:
        emails = PhishingEmailModel.query.all()
        return [PhishingEmailRepository._model_to_entity(email) for email in emails]

    @staticmethod
    def create(recipient_email: str, 
               campaign_id: int, 
               template_id: int, 
               tracking_uuid: str,
               final_subject: str, 
               final_content: str, 
               status: str = "pending") -> PhishingEmail:
        """Creates a new PhishingEmail record including tracking UUID and pre-parsed content."""
        phishing_email_model = PhishingEmailModel(
            recipient_email=recipient_email,
            campaign_id=campaign_id,
            template_id=template_id,
            tracking_uuid=tracking_uuid,
            final_subject=final_subject,
            final_content=final_content,
            status=status
        )
        db.session.add(phishing_email_model)
        db.session.commit()
        db.session.refresh(phishing_email_model)
        return PhishingEmailRepository._model_to_entity(phishing_email_model)

    @staticmethod
    def update_status(id: int, status: str, error_message: str | None = None) -> PhishingEmail | None:
        """Updates the status and optionally error message of an email."""
        email = PhishingEmailModel.query.get(id)
        if not email:
            print(f"Warning: Phishing email with id {id} not found during status update.")
            return None
        
        email.status = status
        email.error_message = error_message
        if status == "sent":
            email.sent_at = datetime.utcnow()
        
        db.session.commit()
        return PhishingEmailRepository._model_to_entity(email)

    @staticmethod
    def update(phishing_email: PhishingEmail) -> PhishingEmail:
        phishing_email_model = PhishingEmailModel.query.get(phishing_email.id)
        if not phishing_email_model:
            raise ValueError(f"Phishing email with id {phishing_email.id} not found")
        
        phishing_email_model.recipient_email = phishing_email.recipient_email
        phishing_email_model.sent_at = phishing_email.sent_at
        phishing_email_model.status = phishing_email.status
        phishing_email_model.error_message = phishing_email.error_message
        phishing_email_model.campaign_id = phishing_email.campaign_id
        phishing_email_model.template_id = phishing_email.template_id

        db.session.commit()
        return PhishingEmailRepository._model_to_entity(phishing_email_model)

    @staticmethod
    def delete(id: int) -> None:
        PhishingEmailModel.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def _model_to_entity(phishing_email_model: PhishingEmailModel) -> PhishingEmail | None:
        """Converts the SQLAlchemy model to a Pydantic entity."""
        if not phishing_email_model:
            return None
            
        return PhishingEmail(
            id=phishing_email_model.id,
            recipient_email=phishing_email_model.recipient_email,
            sent_at=phishing_email_model.sent_at,
            status=phishing_email_model.status,
            error_message=phishing_email_model.error_message,
            campaign_id=phishing_email_model.campaign_id,
            template_id=phishing_email_model.template_id,
            created_at=phishing_email_model.created_at,
            tracking_uuid=phishing_email_model.tracking_uuid,
            final_subject=phishing_email_model.final_subject,
            final_content=phishing_email_model.final_content
        )
