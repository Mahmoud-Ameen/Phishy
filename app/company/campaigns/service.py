from .entity import Campaign
from .repository import CampaignRepository
from ...phishing.phishing.phishing_service import PhishingService


class CampaignService:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        return CampaignRepository.get_campaigns()

    @staticmethod
    def start_campaign(campaign_name: str, template_id: int, admin_email: str, emails: list[str]):
        """
        Start a new phishing campaign
        Args:
            campaign_name (str): Name of the campaign
            template_id (int): ID of the email template
            admin_email (str): Email of the admin who started the campaign
            emails (list[str]): List of employee emails to send phishing emails to
        Returns:
            Campaign: The newly created campaign  
        """ ""

        # TODO: check if template exists

        camp = CampaignRepository.create_campaign(campaign_name, admin_email)

        # send emails
        PhishingService.send_phishing_emails(emails, template_id, camp.id)

        return camp

