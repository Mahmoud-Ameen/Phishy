from datetime import datetime
from ...extensions import db


class PhishingTargetModel(db.Model):
    __tablename__ = "phishing_targets"
    tracking_key: str = db.Column(db.String(36), primary_key=True)  # UUID
    phishing_email_id: int = db.Column(db.Integer, db.ForeignKey("phishing_emails.id"), nullable=True)
    target_identity: str = db.Column(db.String(255), nullable=False, default="unknown")
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "tracking_key": self.tracking_key,
            "phishing_email_id": self.phishing_email_id,
            "target_identity": self.target_identity,
            "created_at": self.created_at.isoformat()
        }


class EmailOpenModel(db.Model):
    __tablename__ = "email_opens"
    id: int = db.Column(db.Integer, primary_key=True)
    tracking_key: str = db.Column(db.String(36), db.ForeignKey("phishing_targets.tracking_key"), nullable=False)
    ip_address: str = db.Column(db.String(45), nullable=False)  # IPv6 addresses can be up to 45 chars
    user_agent: str = db.Column(db.Text)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat()
        }


class PhishingInteractionModel(db.Model):
    __tablename__ = "phishing_interactions"
    id: int = db.Column(db.Integer, primary_key=True)
    tracking_key: str = db.Column(db.String(36), db.ForeignKey("phishing_targets.tracking_key"), nullable=False)
    interaction_type: str = db.Column(db.String(50), nullable=False)  # click, page_visit, form_submit
    ip_address: str = db.Column(db.String(45), nullable=False)
    user_agent: str = db.Column(db.Text)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tracking_key": self.tracking_key,
            "interaction_type": self.interaction_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat()
        } 