from flask import request, Response
from flask_jwt_extended import jwt_required
from ...core.middlewares.auth import admin_required
from marshmallow import ValidationError
from .repository import ResourceRepository
from .schemas import CreateResourceSchema
from ...core.exceptions import ResourceDoesntExist, ScenarioDoesntExist, DomainDoesntExist, ResourceAlreadyExists
from ...core.response import ApiResponse


class ResourcesController:
    @staticmethod
    @jwt_required()
    def get_resources():
        """Get all phishing resources"""
        resources = ResourceRepository.get_resources()
        return ApiResponse.success({"resources": [resource.to_dict() for resource in resources]})
    
    @staticmethod
    @jwt_required()
    def get_resource(resource_id):
        """Get a specific phishing resource by ID"""
        try:
            resource = ResourceRepository.get_resource_by_id(resource_id)
            return ApiResponse.success({"resource": resource.to_dict()})
        except ResourceDoesntExist:
            return ApiResponse.error("Resource not found", 404)
    
    @staticmethod
    @jwt_required()
    def get_resources_by_scenario(scenario_id):
        """Get all resources for a specific scenario"""
        resources = ResourceRepository.get_resources_by_scenario(scenario_id)
        return ApiResponse.success({"resources": [resource.to_dict() for resource in resources]})
    
    @staticmethod
    @jwt_required()
    def get_resources_by_domain(domain_name):
        """Get all resources for a specific domain"""
        resources = ResourceRepository.get_resources_by_domain(domain_name)
        return ApiResponse.success({"resources": [resource.to_dict() for resource in resources]})
    
    @staticmethod
    @admin_required
    def create_resource():
        """Create a new phishing resource"""
        try:
            data = CreateResourceSchema().load(request.get_json())
            resource = ResourceRepository.create_resource(**data)
            return ApiResponse.success({"resource": resource.to_dict()}, 201)
        except ValidationError as e:
            return ApiResponse.error("Invalid request body", 400, e.messages)
        except ScenarioDoesntExist:
            return ApiResponse.error("Scenario not found", 404)
        except DomainDoesntExist:
            return ApiResponse.error("Domain not found", 404)
        except ResourceAlreadyExists as e:
            return ApiResponse.error(str(e), 409)
    
    @staticmethod
    def serve_resource(domain_name, endpoint):
        """Serve a phishing resource for a given domain and endpoint"""
        print(f"Serving resource for domain: {domain_name} and endpoint: {endpoint}")
        
        resource = ResourceRepository.get_resource_by_domain_and_endpoint(domain_name, endpoint)
        
        if not resource:
            return ApiResponse.error("Resource not found", 404)
        
        return Response(
            resource.content,
            mimetype=resource.content_type
        ) 