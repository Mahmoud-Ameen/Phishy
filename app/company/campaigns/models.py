from app.extensions import db
from datetime import datetime


class CampaignModel(db.Model):
    __tablename__ = "campaigns"
    id: int = db.Column(db.Integer, primary_key=True)
    start_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    name: str = db.Column(db.String(255), nullable=False)
    started_by: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # phishing_emails: Mapped["PhishingEmail"] = db.relationship("PhishingEmail", backref="campaign", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "started_by": self.started_by,
        }
