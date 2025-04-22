from datetime import datetime


class PhishingEmail:
    def __init__(
        self,
        id: int,
        recipient_email: str,
        sent_at: datetime | None,
        status: str,
        error_message: str | None,
        campaign_id: int,
        template_id: int,
        created_at: datetime
    ):
        self.id = id
        self.recipient_email = recipient_email
        self.sent_at = sent_at
        self.status = status
        self.error_message = error_message
        self.campaign_id = campaign_id
        self.template_id = template_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "recipient_email": self.recipient_email,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "status": self.status,
            "error_message": self.error_message,
            "campaign_id": self.campaign_id,
            "template_id": self.template_id,
            "created_at": self.created_at.isoformat()
        }
