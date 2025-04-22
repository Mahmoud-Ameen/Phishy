from datetime import datetime
from .models import PhishingTargetModel, PhishingInteractionModel, EmailOpenModel
from .entity import PhishingTarget, PhishingInteraction, EmailOpen
from ... import db


class PhishingTargetRepository:
    @staticmethod
    def get_by_tracking_key(tracking_key: str) -> PhishingTarget | None:
        model = PhishingTargetModel.query.get(tracking_key)
        return PhishingTargetRepository._model_to_entity(model) if model else None

    @staticmethod
    def get_by_phishing_email_id(phishing_email_id: int) -> list[PhishingTarget]:
        models = PhishingTargetModel.query.filter_by(phishing_email_id=phishing_email_id).all()
        return [PhishingTargetRepository._model_to_entity(model) for model in models]

    @staticmethod
    def create(tracking_key: str, phishing_email_id: int | None, target_identity: str) -> PhishingTarget:
        model = PhishingTargetModel(
            tracking_key=tracking_key,
            phishing_email_id=phishing_email_id,
            target_identity=target_identity
        )
        db.session.add(model)
        db.session.commit()
        return PhishingTargetRepository._model_to_entity(model)

    @staticmethod
    def _model_to_entity(model: PhishingTargetModel) -> PhishingTarget:
        return PhishingTarget(
            tracking_key=model.tracking_key,
            phishing_email_id=model.phishing_email_id,
            target_identity=model.target_identity,
            created_at=model.created_at
        )


class EmailOpenRepository:
    @staticmethod
    def get_by_tracking_key(tracking_key: str) -> list[EmailOpen]:
        models = EmailOpenModel.query.filter_by(tracking_key=tracking_key).all()
        return [EmailOpenRepository._model_to_entity(model) for model in models]

    @staticmethod
    def create(
        tracking_key: str,
        ip_address: str,
        user_agent: str | None = None
    ) -> EmailOpen:
        model = EmailOpenModel(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(model)
        db.session.commit()
        return EmailOpenRepository._model_to_entity(model)

    @staticmethod
    def _model_to_entity(model: EmailOpenModel) -> EmailOpen:
        return EmailOpen(
            id=model.id,
            tracking_key=model.tracking_key,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            timestamp=model.timestamp
        )


class PhishingInteractionRepository:
    @staticmethod
    def get_by_tracking_key(tracking_key: str) -> list[PhishingInteraction]:
        models = PhishingInteractionModel.query.filter_by(tracking_key=tracking_key).all()
        return [PhishingInteractionRepository._model_to_entity(model) for model in models]

    @staticmethod
    def create(
        tracking_key: str,
        interaction_type: str,
        ip_address: str,
        user_agent: str | None = None
    ) -> PhishingInteraction:
        model = PhishingInteractionModel(
            tracking_key=tracking_key,
            interaction_type=interaction_type,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(model)
        db.session.commit()
        return PhishingInteractionRepository._model_to_entity(model)

    @staticmethod
    def _model_to_entity(model: PhishingInteractionModel) -> PhishingInteraction:
        return PhishingInteraction(
            id=model.id,
            tracking_key=model.tracking_key,
            interaction_type=model.interaction_type,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            timestamp=model.timestamp
        ) 