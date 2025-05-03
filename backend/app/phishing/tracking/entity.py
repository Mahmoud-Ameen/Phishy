import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class PhishingInteraction:
    id: int
    tracking_key: str # This is the PhishingEmail.tracking_uuid
    interaction_type: str # e.g., 'email_open', 'resource_visit', 'submission'
    ip_address: str
    user_agent: Optional[str] = None
    interaction_metadata: Optional[str] = None # e.g., '{"form_data": {"username": "testuser", "password": "testpass"}}'
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "interaction_type": self.interaction_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "interaction_metadata": self.interaction_metadata, # Renamed field
            "timestamp": self.timestamp.isoformat()
        }
