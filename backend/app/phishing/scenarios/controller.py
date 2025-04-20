from flask import request
from flask_jwt_extended import jwt_required
from ...core.middlewares.auth import admin_required
from marshmallow import ValidationError
from .service import TemplateService
from ...core.response import ApiResponse
from .schemas import CreateTemplateSchema, CreateScenarioSchema, UpdateTemplateSchema, UpdateScenarioSchema
from .repository import TemplateRepository, ScenarioRepository
from ...core.exceptions import ScenarioDoesntExist, TemplateDoesntExist


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
        scenarios_data = ScenarioRepository.get_scenarios()
        return ApiResponse.success({"scenarios": scenarios_data})

    @staticmethod
    @jwt_required()
    def get_scenario(scenario_id):
        try:
            scenario = ScenarioRepository.get_scenario(scenario_id)
            return ApiResponse.success({"scenario": scenario})
        except ScenarioDoesntExist:
            return ApiResponse.error("Scenario not found", 404)
        except Exception as e:
            print(f"Error fetching scenario {scenario_id}: {e}")
            return ApiResponse.error("Failed to fetch scenario", 500)

    @staticmethod
    @admin_required
    def create_scenario():
        try:
            data = CreateScenarioSchema().load(request.get_json())
            scenario_entity = ScenarioRepository.create_scenario(**data)
            return ApiResponse.success({"scenario": scenario_entity.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except Exception as e:
            print(f"Error creating scenario: {e}")
            return ApiResponse.error("Failed to create scenario", 500)

    @staticmethod
    @admin_required
    def update_scenario(scenario_id):
        try:
            data = UpdateScenarioSchema().load(request.get_json())
            updated_scenario = ScenarioRepository.update_scenario(scenario_id, **data)
            return ApiResponse.success({"scenario": updated_scenario.to_dict()})
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except ScenarioDoesntExist:
            return ApiResponse.error("Scenario not found", 404)
        except Exception as e:
            print(f"Error updating scenario {scenario_id}: {e}")
            return ApiResponse.error("Failed to update scenario", 500)

    @staticmethod
    @admin_required
    def delete_scenario(scenario_id):
        try:
            ScenarioRepository.delete_scenario(scenario_id)
            return ApiResponse.success(message="Scenario deleted successfully")
        except ScenarioDoesntExist:
            return ApiResponse.error("Scenario not found", 404)
        except Exception as e:
            print(f"Error deleting scenario {scenario_id}: {e}")
            return ApiResponse.error("Failed to delete scenario", 500)
