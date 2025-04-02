from datetime import datetime
from .entity import Campaign
from .repository import CampaignRepository
from ...phishing.phishing.phishing_service import PhishingService
from ...core.exceptions import TemplateDoesntExist


class CampaignService:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        return CampaignRepository.get_campaigns()

    @staticmethod
    def start_campaign(campaign_name: str, admin_email: str, emails: list[str], scenario_id: int):
        """
        Start a new phishing campaign
        Args:
            campaign_name (str): Name of the campaign
            admin_email (str): Email of the admin who started the campaign
            emails (list[str]): List of employee emails to send phishing emails to
            scenario_id (int): ID of the phishing scenario to use
        Returns:
            Campaign: The newly created campaign
        Raises:
            TemplateDoesntExist if the template is not found
        """
        # Create campaign
        campaign = CampaignRepository.create_campaign(
            name=campaign_name,
            admin_email=admin_email,
            scenario_id=scenario_id
        )

        try:
            # Send emails using the scenario's template
            PhishingService.send_phishing_emails(emails, scenario_id, campaign.id)
            return campaign

        except Exception as e:
            raise e

    @staticmethod
    def get_campaign_status(campaign_id: int) -> dict:
        """
        Get the current status and statistics of a campaign
        Args:
            campaign_id (int): ID of the campaign
        Returns:
            dict: Campaign status and statistics
        """
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")

        # Get all emails for this campaign
        emails = PhishingService.get_campaign_emails(campaign_id)

        # Calculate statistics
        total_emails = len(emails)
        sent_emails = sum(1 for email in emails if email.status == "sent")
        failed_emails = sum(1 for email in emails if email.status == "failed")
        pending_emails = sum(1 for email in emails if email.status == "pending")

        return {
            "campaign": campaign.to_dict(),
            "statistics": {
                "total_emails": total_emails,
                "sent_emails": sent_emails,
                "failed_emails": failed_emails,
                "pending_emails": pending_emails
            }
        }

