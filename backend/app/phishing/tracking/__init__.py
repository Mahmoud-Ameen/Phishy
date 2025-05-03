from .routes import tracking_bp
from .service import TrackingService
# Remove Target exports
# from .repository import PhishingTargetRepository, PhishingInteractionRepository, EmailOpenRepository
# from .entity import PhishingTarget, PhishingInteraction, EmailOpen

# Keep Interaction and Open exports
from .repository import PhishingInteractionRepository, EmailOpenRepository
from .entity import PhishingInteraction, EmailOpen

__all__ = [
    'tracking_bp', 
    'TrackingService',
    # 'PhishingTarget', # Removed
    'PhishingInteraction', 
    'EmailOpen',
    # 'PhishingTargetRepository', # Removed
    'PhishingInteractionRepository', 
    'EmailOpenRepository'
] 