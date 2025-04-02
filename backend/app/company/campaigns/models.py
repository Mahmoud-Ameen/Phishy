from app.extensions import db
from datetime import datetime


class CampaignModel(db.Model):
    __tablename__ = "campaigns"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    start_date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    started_by: str = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
    scenario_id: int = db.Column(db.Integer, db.ForeignKey("phishing_scenarios.id"), nullable=False)
    # phishing_emails: Mapped["PhishingEmail"] = db.relationship("PhishingEmail", backref="campaign", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "started_by": self.started_by,
            "scenario_id": self.scenario_id
        }
