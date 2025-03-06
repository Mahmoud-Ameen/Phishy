from typing import List
from sqlalchemy.exc import IntegrityError
from ...extensions import db
from .models import DomainModel
from .entity import PhishingDomain
from ...core.exceptions import DomainAlreadyExists


class DomainRepository:
    @staticmethod
    def add_domain(domain_name: str, is_active: bool = True) -> PhishingDomain:
        try:
            domain = DomainModel(domain_name=domain_name, is_active=is_active)
            db.session.add(domain)
            db.session.commit()
            return DomainRepository._model_to_entity(domain)
        except IntegrityError:
            raise DomainAlreadyExists(f"Domain with name {domain_name} already exists")

    @staticmethod
    def get_domains() -> List[PhishingDomain]:
        domains = DomainModel.query.all()
        return [DomainRepository._model_to_entity(domain) for domain in domains]
    
    @staticmethod
    def _model_to_entity(domain: DomainModel) -> PhishingDomain:
        return PhishingDomain(
            domain_name=domain.domain_name,
            is_active=domain.is_active
        ) 