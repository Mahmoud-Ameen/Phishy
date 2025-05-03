from typing import List, Optional, Dict, Any
from datetime import datetime
from ...extensions import db
from .models import PhishingInteractionModel, EmailOpenModel
from .entity import PhishingInteraction, EmailOpen


class PhishingInteractionRepository:
    @staticmethod
    def create(tracking_key: str, interaction_type: str, ip_address: str, 
               user_agent: Optional[str] = None, interaction_metadata: Optional[str] = None) -> PhishingInteraction:
        interaction = PhishingInteractionModel(
            tracking_key=tracking_key,
            interaction_type=interaction_type,
            ip_address=ip_address,
            user_agent=user_agent,
            interaction_metadata=interaction_metadata
        )
        db.session.add(interaction)
        db.session.commit()
        return PhishingInteractionRepository._model_to_entity(interaction)

    @staticmethod
    def get_by_tracking_key(tracking_key: str) -> List[PhishingInteraction]:
        interactions = PhishingInteractionModel.query.filter_by(tracking_key=tracking_key).order_by(PhishingInteractionModel.timestamp.asc()).all()
        return [PhishingInteractionRepository._model_to_entity(i) for i in interactions]

    @staticmethod
    def _model_to_entity(model: PhishingInteractionModel) -> PhishingInteraction:
        return PhishingInteraction(
            id=model.id,
            tracking_key=model.tracking_key,
            interaction_type=model.interaction_type,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            interaction_metadata=model.interaction_metadata,
            timestamp=model.timestamp
        )

class EmailOpenRepository:
    @staticmethod
    def create(tracking_key: str, ip_address: str, user_agent: Optional[str] = None) -> EmailOpen:
        email_open = EmailOpenModel(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(email_open)
        db.session.commit()
        return EmailOpenRepository._model_to_entity(email_open)

    @staticmethod
    def get_by_tracking_key(tracking_key: str) -> List[EmailOpen]:
        opens = EmailOpenModel.query.filter_by(tracking_key=tracking_key).order_by(EmailOpenModel.timestamp.asc()).all()
        return [EmailOpenRepository._model_to_entity(o) for o in opens]

    @staticmethod
    def _model_to_entity(model: EmailOpenModel) -> EmailOpen:
        return EmailOpen(
            id=model.id,
            tracking_key=model.tracking_key,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            timestamp=model.timestamp
        ) 