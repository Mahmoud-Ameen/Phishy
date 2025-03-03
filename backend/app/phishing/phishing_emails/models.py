from datetime import datetime

from ...extensions import db


class PhishingEmailModel(db.Model):
    __tablename__ = "phishing_emails"
    id: int = db.Column(db.Integer, primary_key=True)
    recipient_email: str = db.Column(db.String(255), nullable=False)
    sent_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    campaign_id: int = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    template_id: int = db.Column(db.Integer, db.ForeignKey("phishing_templates.id"))
