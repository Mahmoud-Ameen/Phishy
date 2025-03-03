from .entity import Campaign
from .models import CampaignModel
from app.extensions import db


class CampaignRepository:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        campaigns = CampaignModel.query.all()
        return [CampaignRepository._model_to_entity(campaign) for campaign in campaigns]

    @staticmethod
    def create_campaign(name: str, admin_email: str) -> Campaign:
        campaign = CampaignModel(name=name, started_by=admin_email)
        db.session.add(campaign)
        db.session.commit()
        return CampaignRepository._model_to_entity(campaign)

    @staticmethod
    def _model_to_entity(campaign: CampaignModel) -> Campaign:
        return Campaign(
            id=campaign.id,
            name=campaign.name,
            start_date=str(campaign.start_date),
            started_by=campaign.started_by
        )