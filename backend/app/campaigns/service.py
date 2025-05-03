from app.phishing.scenarios.service import ScenarioService
from app.core.exceptions import OperationFailure
from .entity import Campaign
from .repository import CampaignRepository
from app.phishing.phishing_emails.service import PhishingEmailService
from app.phishing.phishing_emails.repository import PhishingEmailRepository
from flask import current_app


class CampaignService:
    @staticmethod
    def get_campaigns() -> list[Campaign]:
        return CampaignRepository.get_campaigns()

    @staticmethod
    def start_campaign(campaign_name: str, admin_email: str, emails: list[str], scenario_id: int):
        """
        Starts a new phishing campaign.
        1. Validates input and scenario.
        2. Creates the Campaign record in the database.
        3. Tells PhishingEmailService to create records and start background sending.
        4. Handles rollback of Campaign creation if email processing initiation fails.
        5. Returns the created Campaign object immediately if steps 2 & 3 succeed.

        Args:
            campaign_name (str): Name of the campaign
            admin_email (str): Email of the admin who started the campaign
            emails (list[str]): List of employee emails to target
            scenario_id (int): ID of the phishing scenario (implies template)

        Returns:
            Campaign: The newly created campaign object.

        Raises:
            ValueError: If validation fails (e.g., invalid scenario, no emails).
            TemplateDoesntExist: If template is not found for scenario_id.
            OperationFailure: If email processing initiation fails.
            AppException: For other unexpected database errors during campaign creation.
        """

        # Validate recipient emails list
        if not emails:
            raise ValueError("No employee emails provided for campaign")

        # Verify scenario exists and get template
        try:
            template = ScenarioService.get_template_for_scenario(scenario_id)
        except Exception as e:
            raise ValueError(f"Invalid scenario_id {scenario_id} or template issue: {str(e)}")

        campaign = None 
        try:
            # Step 1: Create campaign record
            campaign = CampaignRepository.create_campaign(
                name=campaign_name,
                admin_email=admin_email,
                scenario_id=scenario_id
            )
            print(f"Created Campaign record with ID: {campaign.id}")

            # Step 2: Initiate email record creation and background dispatch
            flask_app = current_app._get_current_object() # Get app context for background tasks
            
            # This call will raise OperationFailure if email record creation fails
            PhishingEmailService.process_campaign_emails(
                campaign_id=campaign.id,
                recipient_emails=emails,
                template_id=template.id,
                app=flask_app
            )
            
            print(f"Successfully initiated email processing for campaign {campaign.id}.")
            # If we reach here, both campaign and email processing initiation were successful
            return campaign

        except (OperationFailure, Exception) as e: # Catch email service failure or DB error
            print(f"Error during campaign start process for campaign '{campaign_name}': {e}")
            # If campaign object was created before the error, try to clean it up
            if campaign and campaign.id:
                print(f"Attempting to clean up campaign {campaign.id} due to error.")
                try:
                    CampaignRepository.delete_campaign(campaign.id)
                    print(f"Cleaned up campaign {campaign.id}.")
                except Exception as cleanup_error:
                    # Log critical error if cleanup fails
                    print(f"CRITICAL: Error during campaign cleanup for {campaign.id}: {cleanup_error}")
            
            # Re-raise the original exception to signal failure
            else: 
                 raise Exception(f"Failed to create campaign or process emails: {e}") 

    @staticmethod
    def get_campaign(campaign_id: int) -> dict:
        """
        Get the campaign details, status, and associated emails.
        Args:
            campaign_id (int): ID of the campaign
        Returns:
            dict: Campaign details, status, and emails
        """
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")

        # Get all emails for this campaign
        emails = PhishingEmailRepository.get_by_campaign_id(campaign_id)
        emails_data = [email.to_dict() for email in emails]

        # Calculate statistics
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
            },
            "emails": emails_data
        }

    @staticmethod
    def get_campaign_emails(campaign_id: int) -> list[dict]:
        """
        Get all phishing emails for a specific campaign
        Args:
            campaign_id (int): ID of the campaign
        Returns:
            list: List of phishing email data
        Raises:
            ValueError: If campaign not found
        """
        # Verify campaign exists
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")
        
        # Get phishing emails
        emails = PhishingEmailRepository.get_by_campaign_id(campaign_id)
        
        # Convert to dict
        return [email.to_dict() for email in emails]

