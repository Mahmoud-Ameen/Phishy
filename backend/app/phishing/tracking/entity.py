import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class PhishingInteraction:
    id: int
    tracking_key: str # This is the PhishingEmail.tracking_uuid
    interaction_type: str # e.g., 'email_open', 'click', 'submission'
    ip_address: str
    user_agent: Optional[str] = None
    interaction_metadata: Optional[str] = None # Renamed field (e.g., JSON string for form data)
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

@dataclass
class EmailOpen:
    id: int
    tracking_key: str # This is the PhishingEmail.tracking_uuid
    ip_address: str
    user_agent: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat()
        }

# --- PhishingTarget removed --- 

# @dataclass
# class PhishingTarget:
#     tracking_key: str
#     phishing_email_id: Optional[int] = None # Link back to the specific email if applicable
#     target_identity: Optional[str] = None # e.g., email address, employee ID, Slack ID
#     created_at: datetime = field(default_factory=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "tracking_key": self.tracking_key,
#             "phishing_email_id": self.phishing_email_id,
#             "target_identity": self.target_identity,
#             "created_at": self.created_at.isoformat()
#         } 