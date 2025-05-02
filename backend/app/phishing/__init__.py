from .scenarios import scenarios_bp, templates_bp
from .domains import domains_bp
from .resources import resources_bp
from .mailer import mailer_bp

__all__ = [
    'templates_bp', 
    'scenarios_bp', 
    'domains_bp', 
    'resources_bp',
    'mailer_bp',
]

"""
Phishing module - responsible for phishing content, templates, tracking, and delivery.

This module focuses on the core mechanics of phishing simulation:
- Email templates (templates/)
- Phishing scenarios combining templates, landing pages, and domains (scenarios/)
- Landing pages and other resources (resources/)
- Domain management (domains/)
- Email sending (mailer/)
- Tracking email opens and clicks (tracking/)
- Recording sent email statuses (phishing_emails/)
"""
