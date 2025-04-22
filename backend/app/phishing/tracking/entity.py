from datetime import datetime


class PhishingTarget:
    def __init__(
        self,
        tracking_key: str,
        phishing_email_id: int | None,
        target_identity: str,
        created_at: datetime
    ):
        self.tracking_key = tracking_key
        self.phishing_email_id = phishing_email_id
        self.target_identity = target_identity
        self.created_at = created_at

    def to_dict(self):
        return {
            "tracking_key": self.tracking_key,
            "phishing_email_id": self.phishing_email_id,
            "target_identity": self.target_identity,
            "created_at": self.created_at.isoformat()
        }


class EmailOpen:
    def __init__(
        self,
        id: int,
        tracking_key: str,
        ip_address: str,
        user_agent: str | None,
        timestamp: datetime
    ):
        self.id = id
        self.tracking_key = tracking_key
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat()
        }


class PhishingInteraction:
    def __init__(
        self,
        id: int,
        tracking_key: str,
        interaction_type: str,
        ip_address: str,
        user_agent: str | None,
        timestamp: datetime
    ):
        self.id = id
        self.tracking_key = tracking_key
        self.interaction_type = interaction_type
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "interaction_type": self.interaction_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat()
        } 