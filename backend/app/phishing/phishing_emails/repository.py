from .models import PhishingEmailModel
from .entity import PhishingEmail
from ... import db


class PhishingEmailRepository:
    @staticmethod
    def get_by_id(id: int) -> PhishingEmail:
        return PhishingEmailRepository._model_to_entity(PhishingEmailModel.query.get(id))

    @staticmethod
    def get_by_recipient_email(recipient_email: str) -> list[PhishingEmail]:
        emails = PhishingEmailModel.query.filter_by(recipient_email=recipient_email).all()
        return [PhishingEmailRepository._model_to_entity(email) for email in emails]

    @staticmethod
    def get_all() -> list[PhishingEmail]:
        emails = PhishingEmailModel.query.all()
        return [PhishingEmailRepository._model_to_entity(email) for email in emails]

    @staticmethod
    def create(recipient_email: str, campaign_id: int, template_id: int) -> PhishingEmail:
        phishing_email_model = PhishingEmailModel(
            recipient_email=recipient_email,
            campaign_id=campaign_id,
            template_id=template_id,
        )
        db.session.add(phishing_email_model)
        db.session.commit()
        return phishing_email_model

    @staticmethod
    def update(phishing_email: PhishingEmail) -> PhishingEmail:
        phishing_email_model = PhishingEmailModel.query.get(phishing_email.id)
        phishing_email_model.recipient_email = phishing_email.recipient_email
        phishing_email_model.sent_at = phishing_email.sent_at
        phishing_email_model.campaign_id = phishing_email.campaign_id
        phishing_email_model.template_id = phishing_email.template_id

        db.session.commit()

        return phishing_email_model

    @staticmethod
    def delete(id: int) -> None:
        PhishingEmailModel.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def _model_to_entity(phishing_email_model: PhishingEmailModel) -> PhishingEmail:
        return PhishingEmail(
            id=phishing_email_model.id,
            recipient_email=phishing_email_model.recipient_email,
            sent_at=phishing_email_model.sent_at,
            campaign_id=phishing_email_model.campaign_id,
            template_id=phishing_email_model.template_id,
        )
