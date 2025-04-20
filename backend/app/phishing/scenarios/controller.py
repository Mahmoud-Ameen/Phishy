from flask import request
from flask_jwt_extended import jwt_required
from ...core.middlewares.auth import admin_required
from marshmallow import ValidationError
from .service import TemplateService
from ...core.response import ApiResponse
from .schemas import CreateTemplateSchema, CreateScenarioSchema, UpdateTemplateSchema, UpdateScenarioSchema
from .repository import TemplateRepository, ScenarioRepository
from ...core.exceptions import ScenarioDoesntExist


class TemplatesController:
    @staticmethod
    @jwt_required()
    def get_templates():
        templates = [t.to_dict() for t in TemplateRepository.get_templates()]
        return ApiResponse.success({"templates": templates})

    @staticmethod
    @admin_required
    def create_template():
        try:
            data = CreateTemplateSchema().load(request.get_json())
            template = TemplateRepository.create_template(
                subject=data['subject'],
                content=data['content'],
                scenario_id=data['scenario_id']
            )
            return ApiResponse.success({"template": template.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except ScenarioDoesntExist as e:
            return ApiResponse.error("Scenario doesn't exist", 400)
        except ValueError as e:
            return ApiResponse.error(str(e), 409)
        except Exception as e:
            print(f"Error creating template: {e}")
            return ApiResponse.error("Failed to create template", 500)

    @staticmethod
    @admin_required
    def update_template(template_id):
        try:
            data = UpdateTemplateSchema().load(request.get_json())
            updated_template = TemplateRepository.update_template(template_id, **data)
            return ApiResponse.success({"template": updated_template.to_dict()})
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except TemplateDoesntExist as e:
            return ApiResponse.error("Template not found", 404)
        except Exception as e:
            print(f"Error updating template {template_id}: {e}")
            return ApiResponse.error("Failed to update template", 500)

    @staticmethod
    @admin_required
    def delete_template(template_id):
        try:
            deleted = TemplateRepository.delete_template(template_id)
            if not deleted:
                return ApiResponse.error("Template not found", 404)
            return ApiResponse.success(message="Template deleted successfully")
        except TemplateDoesntExist as e:
            return ApiResponse.error("Template not found", 404)
        except Exception as e:
            print(f"Error deleting template {template_id}: {e}")
            return ApiResponse.error("Failed to delete template", 500)


class ScenariosController:
    @staticmethod
    @jwt_required()
    def get_scenarios():
        scenarios = ScenarioRepository.get_scenarios()
        return ApiResponse.success({"scenarios": [scenario.to_dict() for scenario in scenarios]})

    @staticmethod
    @admin_required
    def create_scenario():
        try:
            data = CreateScenarioSchema().load(request.get_json())
            scenario = ScenarioRepository.create_scenario(**data)
            return ApiResponse.success({"scenario": scenario.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
