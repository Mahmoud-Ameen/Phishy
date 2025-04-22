from .entity import Campaign
from .repository import CampaignRepository
from ...phishing.phishing.phishing_service import PhishingService
from ...phishing.phishing_emails.repository import PhishingEmailRepository


class CampaignService:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        return CampaignRepository.get_campaigns()

    @staticmethod
    def start_campaign(campaign_name: str, admin_email: str, emails: list[str], scenario_id: int):
        """
        Start a new phishing campaign by creating emails and launching a thread to send them.
        Args:
            campaign_name (str): Name of the campaign
            admin_email (str): Email of the admin who started the campaign
            emails (list[str]): List of employee emails to send phishing emails to
            scenario_id (int): ID of the phishing scenario to use
        Returns:
            Campaign: The newly created campaign
        Raises:
            Any exceptions during campaign creation
        """
        # Create campaign record first
        campaign = CampaignRepository.create_campaign(
            name=campaign_name,
            admin_email=admin_email,
            scenario_id=scenario_id
        )
        
        # Create phishing email records with 'queued' status first
        for recipient in emails:
            PhishingEmailRepository.create(
                recipient_email=recipient,
                campaign_id=campaign.id,
                template_id=scenario_id,  # Assuming template_id = scenario_id or adjust as needed
                # Status is 'pending' by default in the create method
            )
        
        # Start a background thread to process the emails
        try:
            # Start the thread to send emails
            thread = PhishingService.process_campaign_emails_in_background(campaign.id, scenario_id)
            print(f"Started email sending thread for campaign {campaign.id}")
        except Exception as e:
            print(f"Failed to start email sending thread for campaign {campaign.id}: {e}")
            raise e
            
        return campaign

    @staticmethod
    def get_campaign_status(campaign_id: int) -> dict:
        """
        Get the current status and statistics of a campaign.
        Args:
            campaign_id (int): ID of the campaign
        Returns:
            dict: Campaign status and statistics (including delivery and engagement stats)
        """
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")

        emails = PhishingEmailRepository.get_by_campaign_id(campaign_id)

        total_emails = len(emails)
        sent_emails = sum(1 for email in emails if email.status == "sent")
        failed_emails = sum(1 for email in emails if email.status == "failed")
        pending_emails = sum(1 for email in emails if email.status == "pending")
        
        # TODO: Verify these statuses are being set by the tracking service
        opened_emails = sum(1 for email in emails if email.status == "opened")
        clicked_links = sum(1 for email in emails if email.status == "clicked")
        submitted_data = sum(1 for email in emails if email.status == "submitted")

        return {
            "campaign": campaign.to_dict(),
            "status": { 
                "total_emails": total_emails,
                "sent_emails": sent_emails,
                "failed_emails": failed_emails,
                "pending_emails": pending_emails,
                "opened_emails": opened_emails, 
                "clicked_links": clicked_links,
                "submitted_data": submitted_data
            }
        }

