from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.core.exceptions import DomainAlreadyExists, ScenarioDoesntExist
from app.core.middlewares.auth import admin_required
from .service import TemplateService
from ...core.response import ApiResponse
from .schemas import CreateTemplateSchema, CreateScenarioSchema, CreateDomainSchema
from .repository import TemplateRepository, ScenarioRepository, DomainRepository


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
            data = CreateTemplateSchema().load(request.get_json())
            template = TemplateRepository.create_template(**data)
            return ApiResponse.success({"template": template.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except ScenarioDoesntExist as e:
            return ApiResponse.error("Scenario doesn't exist", 400)


class ScenariosController:
    @staticmethod
    def get_scenarios():
        scenarios = ScenarioRepository.get_scenarios()
        return ApiResponse.success({"scenarios": [scenario.to_dict() for scenario in scenarios]})

    @staticmethod
    def create_scenario():
        try:
            data = CreateScenarioSchema().load(request.get_json())
            scenario = ScenarioRepository.create_scenario(**data)
            return ApiResponse.success({"scenario": scenario.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)


class DomainsController:
    @staticmethod
    def get_domains():
        domains = DomainRepository.get_domains()
        return ApiResponse.success({"domains": [domain.to_dict() for domain in domains]})

    @staticmethod
    @admin_required
    def create_domain():
        try:
            data = request.get_json()
            schema = CreateDomainSchema(**data)
            domain = DomainRepository.add_domain(**schema.model_dump())
            return ApiResponse.success({"domain": domain.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except DomainAlreadyExists as e:
            return ApiResponse.error("Domain already exists", 400)
