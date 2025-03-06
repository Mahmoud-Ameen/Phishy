from flask import request
from flask_jwt_extended import jwt_required
from ...core.middlewares.auth import admin_required
from marshmallow import ValidationError
from .repository import DomainRepository
from .schemas import CreateDomainSchema
from ...core.exceptions import DomainAlreadyExists
from ...core.response import ApiResponse


class DomainsController:
    @staticmethod
    def get_domains():
        domains = DomainRepository.get_domains()
        return ApiResponse.success({"domains": [domain.to_dict() for domain in domains]})

    @staticmethod
    @admin_required
    def create_domain():
        try:
            data = CreateDomainSchema().load(request.get_json())
            domain = DomainRepository.add_domain(**data)
            return ApiResponse.success({"domain": domain.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except DomainAlreadyExists as e:
            return ApiResponse.error("Domain already exists", 400) 