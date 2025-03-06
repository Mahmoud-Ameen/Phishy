from ...extensions import db
from datetime import datetime
from sqlalchemy import UniqueConstraint


class PhishingResourceModel(db.Model):
    __tablename__ = "phishing_resources"
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('phishing_scenarios.id'), nullable=False)
    domain_name = db.Column(db.String(255), db.ForeignKey('domains.domain_name'), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add unique constraint for domain_name and endpoint combination
    __table_args__ = (
        UniqueConstraint('domain_name', 'endpoint', name='uix_domain_endpoint'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'domain_name': self.domain_name,
            'endpoint': self.endpoint,
            'content': self.content,
            'content_type': self.content_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 