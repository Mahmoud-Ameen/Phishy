from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.core.middlewares.auth import admin_required
from .service import TemplateService
from ...core.response import ApiResponse
from .schemas import CreateTemplateSchema


class TemplatesController:
    @staticmethod
    @jwt_required()
    def get_templates():
        templates = [t.to_dict() for t in TemplateService.get_templates()]
        return ApiResponse.success({"templates": templates})

    @staticmethod
    @admin_required
    def create_template():
        try:
            data = request.get_json()
            data = CreateTemplateSchema().load(data)

            template = TemplateService.create_template(data['subject'], data['content'], data['level'])
            return ApiResponse.success(
                {"template": template.to_dict()},
                "Template created successfully"
            )
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
