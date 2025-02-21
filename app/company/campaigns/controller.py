from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

# app specific
from app.core.middlewares.auth import admin_required
from app.core.response import ApiResponse
from .schemas import CreateCampaignSchema
from .service import CampaignService
from ...core.exceptions import TemplateDoesntExist


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
            campaign = CampaignService.start_campaign(campaign_name=data["name"],
                                                      admin_email=user_email,
                                                      template_id=data["template_id"],
                                                      emails=data["employee_emails"])
            return ApiResponse.success(
                {"campaign": campaign},
                "Campaign started successfully"
            )
        except ValidationError as e:
            return ApiResponse.error("Invalid input body", 400, e.messages)
        except TemplateDoesntExist:
            return ApiResponse.error("Template does not exist", 400)
