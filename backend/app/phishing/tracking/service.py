from typing import Optional, List, Dict, Any
import json
from flask import current_app
from .entity import PhishingInteraction
from .repository import PhishingInteractionRepository


class TrackingService:
    """Handles recording interactions and updating email status based on tracking keys (UUIDs)."""

    @staticmethod
    def generate_tracking_pixel_url(tracking_key: str) -> str:
        """Generates the full URL for the tracking pixel."""
        base_url = current_app.config.get('TRACKING_URL', '/api/tracking/open')
        print(f"Tracking URL used when generating tracking pixel URL: {base_url}/{tracking_key}")
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        return f"{base_url}/{tracking_key}"

    @staticmethod
    def track_interaction(tracking_key: str, 
                            interaction_type: str, 
                            ip_address: str, 
                            user_agent: Optional[str] = None, 
                            form_data: Optional[Dict[str, Any]] = None):
        """
        Records an interaction (open, click, submission) based on the tracking key (UUID).
        Updates the corresponding PhishingEmail record's status.
        Assumes tracking_key is the PhishingEmail.tracking_uuid.
        """
        print(f"Tracking interaction: key={tracking_key}, type={interaction_type}, ip={ip_address}")
        
        # 1. Record Interaction Details
        metadata_str = json.dumps(form_data) if form_data else None
        try:
            interaction = PhishingInteractionRepository.create(
                tracking_key=tracking_key, 
                interaction_type=interaction_type,
                ip_address=ip_address,
                user_agent=user_agent,
                interaction_metadata=metadata_str
            )
            print(f"Interaction recorded: {interaction.id}")
            
        except Exception as e:
            print(f"Error recording interaction details for key {tracking_key}: {e}")


    @staticmethod
    def get_interactions_by_tracking_key(tracking_key: str) -> List[PhishingInteraction]:
        """
        Get all interactions for a tracking key (UUID)
        """
        return PhishingInteractionRepository.get_by_tracking_key(tracking_key)
