from dataclasses import dataclass
from datetime import datetime


@dataclass
class PhishingEmail:
    id: int
    recipient_email: str
    sent_at: datetime
    campaign_id: int
    template_id: int
