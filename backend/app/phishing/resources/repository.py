from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from ...extensions import db
from .models import PhishingResourceModel
from .entity import PhishingResource
from ...core.exceptions import ResourceDoesntExist, ScenarioDoesntExist, DomainDoesntExist, ResourceAlreadyExists
from ..scenarios.models import ScenarioModel
from ..domains.models import DomainModel


class ResourceRepository:
    @staticmethod
    def create_resource(
        scenario_id: int,
        domain_name: str,
        endpoint: str,
        content: str,
        content_type: str
    ) -> PhishingResource:
        """
        Create and store a phishing resource
        
        Args:
            scenario_id: ID of the scenario this resource belongs to
            domain_name: Domain name for this resource
            endpoint: URL endpoint (e.g., "login")
            content: Content of the resource (HTML, JSON, etc.)
            content_type: MIME type of the content
            
        Returns:
            PhishingResource entity
            
        Raises:
            ScenarioDoesntExist: if scenario_id doesn't exist
            DomainDoesntExist: if domain_name doesn't exist
            ResourceAlreadyExists: if a resource with the same domain_name and endpoint already exists
        """
        # Verify scenario exists
        scenario = ScenarioModel.query.get(scenario_id)
        if not scenario:
            raise ScenarioDoesntExist(f"Scenario with id {scenario_id} not found")
            
        # Verify domain exists
        domain = DomainModel.query.filter_by(domain_name=domain_name).first()
        if not domain:
            raise DomainDoesntExist(f"Domain with name {domain_name} not found")
        
        # Remove leading/trailing slashes if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]
        
        # Check if resource with same domain and endpoint already exists
        existing_resource = ResourceRepository.get_resource_by_domain_and_endpoint(domain_name, endpoint)
        if existing_resource:
            raise ResourceAlreadyExists(f"Resource with domain '{domain_name}' and endpoint '{endpoint}' already exists")
        
        try:
            resource = PhishingResourceModel(
                scenario_id=scenario_id,
                domain_name=domain_name,
                endpoint=endpoint,
                content=content,
                content_type=content_type
            )
            db.session.add(resource)
            db.session.commit()
            return ResourceRepository._model_to_entity(resource)
        except IntegrityError:
            db.session.rollback()
            raise ResourceAlreadyExists(f"Resource with domain '{domain_name}' and endpoint '{endpoint}' already exists")
    
    @staticmethod
    def get_resources() -> List[PhishingResource]:
        """Get all phishing resources"""
        resources = PhishingResourceModel.query.all()
        return [ResourceRepository._model_to_entity(resource) for resource in resources]
    
    @staticmethod
    def get_resource_by_id(resource_id: int) -> PhishingResource:
        """
        Get a phishing resource by its id
        
        Args:
            resource_id: Resource ID
            
        Returns:
            PhishingResource entity
            
        Raises:
            ResourceDoesntExist: if resource is not found
        """
        resource = PhishingResourceModel.query.get(resource_id)
        if not resource:
            raise ResourceDoesntExist(f"Resource with id {resource_id} not found")
        return ResourceRepository._model_to_entity(resource)
    
    @staticmethod
    def get_resources_by_scenario(scenario_id: int) -> List[PhishingResource]:
        """Get all resources for a specific scenario"""
        resources = PhishingResourceModel.query.filter_by(scenario_id=scenario_id).all()
        return [ResourceRepository._model_to_entity(resource) for resource in resources]
    
    @staticmethod
    def get_resources_by_domain(domain_name: str) -> List[PhishingResource]:
        """Get all resources for a specific domain"""
        resources = PhishingResourceModel.query.filter_by(domain_name=domain_name).all()
        return [ResourceRepository._model_to_entity(resource) for resource in resources]
    
    @staticmethod
    def get_resource_by_domain_and_endpoint(domain_name: str, endpoint: str) -> Optional[PhishingResource]:
        """
        Get a resource by domain name and endpoint
        
        Args:
            domain_name: Domain name
            endpoint: URL endpoint
            
        Returns:
            PhishingResource entity or None if not found
        """
        # Remove leading slash if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
            
        resource = PhishingResourceModel.query.filter_by(
            domain_name=domain_name,
            endpoint=endpoint
        ).first()
        
        if not resource:
            return None
            
        return ResourceRepository._model_to_entity(resource)
    
    @staticmethod
    def _model_to_entity(resource: PhishingResourceModel) -> PhishingResource:
        return PhishingResource(
            id=resource.id,
            scenario_id=resource.scenario_id,
            domain_name=resource.domain_name,
            endpoint=resource.endpoint,
            content=resource.content,
            content_type=resource.content_type,
            created_at=resource.created_at
        ) 