from typing import List, Optional, Dict, Any
from ...extensions import db
from .models import PhishingInteractionModel
from .entity import PhishingInteraction


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
    def get_all() -> List[PhishingInteraction]:
        interactions = PhishingInteractionModel.query.order_by(PhishingInteractionModel.timestamp.asc()).all()
        return [PhishingInteractionRepository._model_to_entity(i) for i in interactions]

    @staticmethod
    def get_count_by_tracking_key(tracking_key: str) -> int:
        count = PhishingInteractionModel.query.filter_by(tracking_key=tracking_key).count()
        return count

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

