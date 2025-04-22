import uuid
from datetime import datetime
from typing import Optional, List
from .entity import PhishingTarget, PhishingInteraction, EmailOpen
from .repository import PhishingTargetRepository, PhishingInteractionRepository, EmailOpenRepository


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
    def record_email_open(
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
        return EmailOpenRepository.create(
            tracking_key=tracking_key,
            ip_address=ip_address,
            user_agent=user_agent
        )

    @staticmethod
    def record_interaction(
        tracking_key: str,
        interaction_type: str,
        ip_address: str,
        user_agent: Optional[str] = None
    ) -> PhishingInteraction:
        """
        Record a phishing interaction (email open, click, etc.)
        Args:
            tracking_key: The tracking key associated with the interaction
            interaction_type: Type of interaction (email_open, click, etc.)
            ip_address: IP address of the interaction
            user_agent: User agent string of the interaction
        Returns:
            PhishingInteraction: The recorded interaction
        """
        return PhishingInteractionRepository.create(
            tracking_key=tracking_key,
            interaction_type=interaction_type,
            ip_address=ip_address,
            user_agent=user_agent
        ) 