from flask_jwt_extended import jwt_required

# app specific
from app.core.middlewares.auth import admin_required
from app.core.response import ApiResponse
from .service import CampaignService


class CampaignsController:
    @staticmethod
    @jwt_required()
    def get_campaigns():
        campaigns = CampaignService.get_campaigns()
        return ApiResponse.success({"campaigns": campaigns})

    @staticmethod
    @admin_required
    def start_campaign():
        campaign = CampaignService.start_campaign()
        return ApiResponse.success(
            {"campaign": campaign},
            "Campaign started successfully"
        )
