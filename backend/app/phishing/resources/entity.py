from dataclasses import dataclass
from datetime import datetime


@dataclass
class PhishingResource:
    id: int
    scenario_id: int
    domain_name: str
    endpoint: str
    content: str
    content_type: str
    created_at: datetime | None = None

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'domain_name': self.domain_name,
            'endpoint': self.endpoint,
            'content': self.content,
            'content_type': self.content_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 