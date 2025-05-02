import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from .entity import PhishingTarget, PhishingInteraction, EmailOpen
from .repository import PhishingTargetRepository, PhishingInteractionRepository, EmailOpenRepository
from app.phishing.phishing_emails.repository import PhishingEmailRepository


class TrackingService:
    @staticmethod
    def generate_tracking_key(phishing_email_id: int | None, target_identity: str) -> str:
        """
        Generate a unique tracking key for a phishing target
        Args:
            phishing_email_id: ID of the phishing email (can be None for non-email targets)
            target_identity: Identity of the target (email, etc.)
        Returns:
            str: The generated tracking key
        """
        # Generate a unique tracking key
        tracking_key = str(uuid.uuid4())
        
        # Store in database
        PhishingTargetRepository.create(
            tracking_key=tracking_key,
            phishing_email_id=phishing_email_id,
            target_identity=target_identity
        )
        
        return tracking_key

    @staticmethod
    def get_target_by_tracking_key(tracking_key: str) -> Optional[PhishingTarget]:
        """
        Get a phishing target by its tracking key
        Args:
            tracking_key: The tracking key to look up
        Returns:
            PhishingTarget | None: The target if found, None otherwise
        """
        return PhishingTargetRepository.get_by_tracking_key(tracking_key)

    @staticmethod
    def get_targets_by_phishing_email(phishing_email_id: int):
        """
        Get all targets associated with a phishing email
        Args:
            phishing_email_id: ID of the phishing email
        Returns:
            list[PhishingTarget]: List of targets
        """
        return PhishingTargetRepository.get_by_phishing_email_id(phishing_email_id)

    @staticmethod
    def get_interactions_by_tracking_key(tracking_key: str) -> List[PhishingInteraction]:
        """
        Get all interactions for a tracking key
        Args:
            tracking_key: The tracking key to look up
        Returns:
            list[PhishingInteraction]: List of interactions
        """
        return PhishingInteractionRepository.get_by_tracking_key(tracking_key)

    @staticmethod
    def get_email_opens_by_tracking_key(tracking_key: str) -> List[EmailOpen]:
        """
        Get all email opens for a tracking key
        Args:
            tracking_key: The tracking key to look up
        Returns:
            list[EmailOpen]: List of email opens
        """
        return EmailOpenRepository.get_by_tracking_key(tracking_key)

    @staticmethod
    def record_open(
        tracking_key: str,
        ip_address: str,
        user_agent: Optional[str] = None
    ) -> EmailOpen:
        """
        Record an email open
        Args:
            tracking_key: The tracking key associated with the email open
            ip_address: IP address of the email open
            user_agent: User agent string of the email open
        Returns:
            EmailOpen: The recorded email open
        """
        # Record in email_opens table
        open_record = EmailOpenRepository.create(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Record in interactions table
        TrackingService.record_interaction(
            tracking_key=tracking_key,
            interaction_type="email_open",
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Update the phishing_email status if exists
        target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
        if target and target.phishing_email_id:
            PhishingEmailRepository.update_status(target.phishing_email_id, "opened")
            
        return open_record

    @staticmethod
    def record_click(
        tracking_key: str,
        ip_address: str,
        user_agent: Optional[str] = None
    ) -> PhishingInteraction:
        """
        Record a link click
        Args:
            tracking_key: The tracking key associated with the click
            ip_address: IP address of the click
            user_agent: User agent string of the click
        Returns:
            PhishingInteraction: The recorded interaction
        """
        interaction = TrackingService.record_interaction(
            tracking_key=tracking_key,
            interaction_type="click",
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Update the phishing_email status if exists
        target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
        if target and target.phishing_email_id:
            PhishingEmailRepository.update_status(target.phishing_email_id, "clicked")
            
        return interaction

    @staticmethod
    def record_submission(
        tracking_key: str,
        ip_address: str,
        user_agent: Optional[str] = None,
        form_data: Optional[Dict[str, Any]] = None
    ) -> PhishingInteraction:
        """
        Record a form submission
        Args:
            tracking_key: The tracking key associated with the submission
            ip_address: IP address of the submission
            user_agent: User agent string of the submission
            form_data: Form data submitted
        Returns:
            PhishingInteraction: The recorded interaction
        """
        # Convert form_data to string if provided
        metadata = None
        if form_data:
            import json
            metadata = json.dumps(form_data)
            
        interaction = TrackingService.record_interaction(
            tracking_key=tracking_key,
            interaction_type="submission",
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata
        )
        
        # Update the phishing_email status if exists
        target = PhishingTargetRepository.get_by_tracking_key(tracking_key)
        if target and target.phishing_email_id:
            PhishingEmailRepository.update_status(target.phishing_email_id, "submitted")
            
        return interaction

    @staticmethod
    def record_interaction(
        tracking_key: str,
        interaction_type: str,
        ip_address: str,
        user_agent: Optional[str] = None,
        metadata: Optional[str] = None
    ) -> PhishingInteraction:
        """
        Record a phishing interaction (email open, click, etc.)
        Args:
            tracking_key: The tracking key associated with the interaction
            interaction_type: Type of interaction (email_open, click, etc.)
            ip_address: IP address of the interaction
            user_agent: User agent string of the interaction
            metadata: Optional additional data about the interaction
        Returns:
            PhishingInteraction: The recorded interaction
        """
        return PhishingInteractionRepository.create(
            tracking_key=tracking_key,
            interaction_type=interaction_type,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata
        ) 