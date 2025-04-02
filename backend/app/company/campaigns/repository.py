from datetime import datetime
from .entity import Campaign
from .models import CampaignModel
from app.extensions import db


class CampaignRepository:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        campaigns = CampaignModel.query.all()
        return [CampaignRepository._model_to_entity(campaign) for campaign in campaigns]

    @staticmethod
    def get_campaign_by_id(id: int) -> Campaign | None:
        campaign = CampaignModel.query.get(id)
        return CampaignRepository._model_to_entity(campaign) if campaign else None

    @staticmethod
    def create_campaign(name: str, admin_email: str, scenario_id: int) -> Campaign:
        campaign = CampaignModel(
            name=name,
            started_by=admin_email,
            scenario_id=scenario_id
        )
        db.session.add(campaign)
        db.session.commit()
        return CampaignRepository._model_to_entity(campaign)

    @staticmethod
    def _model_to_entity(campaign_model: CampaignModel) -> Campaign:
        return Campaign(
            id=campaign_model.id,
            name=campaign_model.name,
            start_date=campaign_model.start_date,
            started_by=campaign_model.started_by,
            scenario_id=campaign_model.scenario_id
        )