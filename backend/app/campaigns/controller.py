from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

# app specific
from app.core.middlewares.auth import admin_required
from app.core.response import ApiResponse
from app.campaigns.schemas import CreateCampaignSchema
from app.campaigns.service import CampaignService
from app.core.exceptions import TemplateDoesntExist


class CampaignsController:
    @staticmethod
    @jwt_required()
    def get_campaigns():
        campaigns = CampaignService.get_campaigns()
        campaigns = [camp.to_dict() for camp in campaigns]
        return ApiResponse.success({"campaigns": campaigns})

    @staticmethod
    @admin_required
    def start_campaign():
        try:
            # validate request
            data = request.get_json()
            CreateCampaignSchema().load(data)

            # start campaign
            user_email = get_jwt_identity()
            campaign = CampaignService.start_campaign(
                campaign_name=data["name"],
                admin_email=user_email,
                emails=data["employee_emails"],
                scenario_id=data["scenario_id"]
            )
            return ApiResponse.success(
                {"campaign": campaign.to_dict()},
                "Campaign created successfully",
            )
        except ValidationError as e:
            return ApiResponse.error("Invalid input body", 400, e.messages)
        except TemplateDoesntExist:
            return ApiResponse.error("Template does not exist for the selected scenario", 400)
        except ValueError as e:
            return ApiResponse.error(str(e), 400)
        except Exception as e:
            print("Error starting campaign:", e)
            return ApiResponse.error("Failed to start campaign", 500)

    @staticmethod
    @jwt_required()
    def get_campaign(campaign_id: int):
        try:
            campaign_data = CampaignService.get_campaign(campaign_id)
            return ApiResponse.success(campaign_data)
        except ValueError as e:
            return ApiResponse.error(str(e), 404)
        except Exception as e:
            print(f"Error getting campaign {campaign_id}: {e}")
            return ApiResponse.error("Failed to retrieve campaign details", 500)

    @staticmethod
    @jwt_required()
    def get_campaign_emails(campaign_id: int):
        """Get all phishing emails for a campaign"""
        try:
            emails = CampaignService.get_campaign_emails(campaign_id)
            return ApiResponse.success({"emails": emails})
        except ValueError as e:
            return ApiResponse.error(str(e), 404)
