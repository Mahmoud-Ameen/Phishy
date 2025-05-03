from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ...extensions import db


class PhishingInteractionModel(db.Model):
    __tablename__ = "phishing_interactions"
    id = Column(Integer, primary_key=True)
    # No direct FK, relies on PhishingEmail.tracking_uuid
    tracking_key = Column(String(36), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False) # e.g., 'email_open', 'click', 'submission'
    ip_address = Column(String(45)) 
    user_agent = Column(String(255))
    interaction_metadata = Column(Text, nullable=True) # e.g., JSON string for form data
    timestamp = Column(DateTime, default=datetime.utcnow)

class EmailOpenModel(db.Model):
    __tablename__ = "email_opens"
    id = Column(Integer, primary_key=True)
    # No direct FK, relies on PhishingEmail.tracking_uuid
    tracking_key = Column(String(36), nullable=False, index=True)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
