from datetime import datetime
import uuid

from ...extensions import db


class PhishingEmailModel(db.Model):
    __tablename__ = "phishing_emails"
    id: int = db.Column(db.Integer, primary_key=True)
    tracking_uuid: str = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    recipient_email: str = db.Column(db.String(255), nullable=False)
    sent_at: datetime = db.Column(db.DateTime, nullable=True)
    status: str = db.Column(db.String(50), default="pending")  # pending, sent, failed
    error_message: str = db.Column(db.Text, nullable=True)
    campaign_id: int = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    template_id: int = db.Column(db.Integer, db.ForeignKey("phishing_templates.id"))
    final_subject: str = db.Column(db.String(500), nullable=False)
    final_content: str = db.Column(db.Text, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "recipient_email": self.recipient_email,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "status": self.status,
            "error_message": self.error_message,
            "campaign_id": self.campaign_id,
            "template_id": self.template_id,
            "created_at": self.created_at.isoformat(),
            "tracking_uuid": self.tracking_uuid,
            "final_subject": self.final_subject,
            "final_content": self.final_content,
        }
