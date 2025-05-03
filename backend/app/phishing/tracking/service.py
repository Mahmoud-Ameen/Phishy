import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from .entity import PhishingInteraction, EmailOpen
from .repository import PhishingInteractionRepository, EmailOpenRepository
from app.phishing.phishing_emails.repository import PhishingEmailRepository


class TrackingService:
    """Handles recording interactions and updating email status based on tracking keys (UUIDs)."""

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
            
            if interaction_type == "email_open":
                EmailOpenRepository.create(
                    tracking_key=tracking_key,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                print(f"EmailOpen recorded for key {tracking_key}")

        except Exception as e:
            print(f"Error recording interaction details for key {tracking_key}: {e}")
            # Decide if failure here should prevent status update (probably not)

        # 2. Update PhishingEmail Status
        try:
            # Find PhishingEmail directly by the UUID (which is the tracking_key)
            email_record = PhishingEmailRepository.get_by_tracking_uuid(tracking_key)
            
            if email_record:
                # Determine new status based on interaction type
                # NOTE: Should use Enum for status comparison and setting
                current_status = email_record.status
                new_status = None
                # Define status progression logic
                if interaction_type == "email_open" and current_status in ["sent", "pending"]:
                    new_status = "opened"
                elif interaction_type == "click" and current_status in ["sent", "pending", "opened"]:
                    new_status = "clicked"
                elif interaction_type == "submission": # Submission implies open/click
                    new_status = "submitted"
                
                # Update only if the new status is more advanced or relevant
                if new_status and new_status != current_status: # Add logic if status order matters
                    print(f"Updating status for PhishingEmail ID {email_record.id} from {current_status} to {new_status}")
                    PhishingEmailRepository.update_status(email_record.id, new_status)
                else:
                    print(f"No status update needed for email {email_record.id} (current: {current_status}, interaction: {interaction_type})")
            else:
                # This is expected if the tracking_key is for a non-email target (if supported later)
                # or if the key is invalid.
                print(f"Warning: No PhishingEmail found for tracking key {tracking_key} during interaction update.")
        except Exception as e:
            print(f"Error updating PhishingEmail status for key {tracking_key}: {e}")

    @staticmethod
    def get_interactions_by_tracking_key(tracking_key: str) -> List[PhishingInteraction]:
        """
        Get all interactions for a tracking key (UUID)
        """
        return PhishingInteractionRepository.get_by_tracking_key(tracking_key)

    @staticmethod
    def get_email_opens_by_tracking_key(tracking_key: str) -> List[EmailOpen]:
        """
        Get all email opens for a tracking key (UUID)
        """
        return EmailOpenRepository.get_by_tracking_key(tracking_key)

    # --- Deprecated/Removed Methods --- 
    # The following methods might be replaced or removed as the logic is now in track_interaction
    # and the PhishingTarget entity might become obsolete if tracking_uuid is directly on PhishingEmail.
    # 
    # @staticmethod
    # def get_target_by_tracking_key(tracking_key: str) -> Optional[PhishingTarget]: ...
    # 
    # @staticmethod
    # def get_targets_by_phishing_email(phishing_email_id: int): ...

    # --- Keep helper/getter methods if still needed --- 
    # (get_target_by_tracking_key, get_targets_by_phishing_email etc. might need removal or updates 
    # if PhishingTarget entity/repo are removed/changed)
    # For now, let's assume they are still needed elsewhere or will be cleaned up later.

    # @staticmethod
    # def get_target_by_tracking_key(tracking_key: str) -> Optional[PhishingTarget]:
    #     """
    #     Get a phishing target by its tracking key
    #     Args:
    #         tracking_key: The tracking key to look up
    #     Returns:
    #         PhishingTarget | None: The target if found, None otherwise
    #     """
    #     return PhishingTargetRepository.get_by_tracking_key(tracking_key)

    # @staticmethod
    # def get_targets_by_phishing_email(phishing_email_id: int):
    #     """
    #     Get all targets associated with a phishing email
    #     Args:
    #         phishing_email_id: ID of the phishing email
    #     Returns:
    #         list[PhishingTarget]: List of targets
    #     """
    #     return PhishingTargetRepository.get_by_phishing_email_id(phishing_email_id)

    # @staticmethod
    # def get_interactions_by_tracking_key(tracking_key: str) -> List[PhishingInteraction]:
    #     """
    #     Get all interactions for a tracking key
    #     Args:
    #         tracking_key: The tracking key to look up
    #     Returns:
    #         list[PhishingInteraction]: List of interactions
    #     """
    #     return PhishingInteractionRepository.get_by_tracking_key(tracking_key)

    # @staticmethod
    # def get_email_opens_by_tracking_key(tracking_key: str) -> List[EmailOpen]:
    #     """
    #     Get all email opens for a tracking key
    #     Args:
    #         tracking_key: The tracking key to look up
    #     Returns:
    #         list[EmailOpen]: List of email opens
    #     """
    #     return EmailOpenRepository.get_by_tracking_key(tracking_key)

    # @staticmethod
    # def record_open(
    #     tracking_key: str,
    #     ip_address: str,
    #     user_agent: Optional[str] = None
    # ) -> EmailOpen:
    #     """
    #     Record an email open
    #     Args:
    #         tracking_key: The tracking key associated with the email open
    #         ip_address: IP address of the email open
    #         user_agent: User agent string of the email open
    #     Returns:
    #         EmailOpen: The recorded email open
    #     """
    #     # Record in email_opens table
    #     open_record = EmailOpenRepository.create(
    #         tracking_key=tracking_key,
    #         ip_address=ip_address,
    #         user_agent=user_agent
    #     )
    #     
    #     # Record in interactions table
    #     TrackingService.record_interaction(
    #         tracking_key=tracking_key,
    #         interaction_type="email_open",
    #         ip_address=ip_address,
    #         user_agent=user_agent
    #     )
    #     
    #     # Update the phishing_email status if exists
    #     target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
    #     if target and target.phishing_email_id:
    #         PhishingEmailRepository.update_status(target.phishing_email_id, "opened")
    #         
    #     return open_record

    # @staticmethod
    # def record_click(
    #     tracking_key: str,
    #     ip_address: str,
    #     user_agent: Optional[str] = None
    # ) -> PhishingInteraction:
    #     """
    #     Record a link click
    #     Args:
    #         tracking_key: The tracking key associated with the click
    #         ip_address: IP address of the click
    #         user_agent: User agent string of the click
    #     Returns:
    #         PhishingInteraction: The recorded interaction
    #     """
    #     interaction = TrackingService.record_interaction(
    #         tracking_key=tracking_key,
    #         interaction_type="click",
    #         ip_address=ip_address,
    #         user_agent=user_agent
    #     )
    #     
    #     # Update the phishing_email status if exists
    #     target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
    #     if target and target.phishing_email_id:
    #         PhishingEmailRepository.update_status(target.phishing_email_id, "clicked")
    #         
    #     return interaction

    # @staticmethod
    # def record_submission(
    #     tracking_key: str,
    #     ip_address: str,
    #     user_agent: Optional[str] = None,
    #     form_data: Optional[Dict[str, Any]] = None
    # ) -> PhishingInteraction:
    #     """
    #     Record a form submission
    #     Args:
    #         tracking_key: The tracking key associated with the submission
    #         ip_address: IP address of the submission
    #         user_agent: User agent string of the submission
    #         form_data: Form data submitted
    #     Returns:
    #         PhishingInteraction: The recorded interaction
    #     """
    #     # Convert form_data to string if provided
    #     metadata = None
    #     if form_data:
    #         import json
    #         metadata = json.dumps(form_data)
    #         
    #     interaction = TrackingService.record_interaction(
    #         tracking_key=tracking_key,
    #         interaction_type="submission",
    #         ip_address=ip_address,
    #         user_agent=user_agent,
    #         metadata=metadata
    #     )
    #     
    #     # Update the phishing_email status if exists
    #     target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
    #     if target and target.phishing_email_id:
    #         PhishingEmailRepository.update_status(target.phishing_email_id, "submitted")
    #         
    #     return interaction

    # @staticmethod
    # def record_interaction(
    #     tracking_key: str,
    #     interaction_type: str,
    #     ip_address: str,
    #     user_agent: Optional[str] = None,
    #     metadata: Optional[str] = None
    # ) -> PhishingInteraction:
    #     """
    #     Record a phishing interaction (email open, click, etc.)
    #     Args:
    #         tracking_key: The tracking key associated with the interaction
    #         interaction_type: Type of interaction (email_open, click, etc.)
    #         ip_address: IP address of the interaction
    #         user_agent: User agent string of the interaction
    #         metadata: Optional additional data about the interaction
    #     Returns:
    #         PhishingInteraction: The recorded interaction
    #     """
    #     return PhishingInteractionRepository.create(
    #         tracking_key=tracking_key,
    #         interaction_type=interaction_type,
    #         ip_address=ip_address,
    #         user_agent=user_agent,
    #         metadata=metadata
    #     ) 