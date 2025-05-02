from app.phishing.scenarios.service import ScenarioService
from app.core.exceptions import AppException
from .entity import Campaign
from .repository import CampaignRepository
from app.phishing.mailer.mailer_service import PhishingEmailManager
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
        3. Creates all associated PhishingEmail records with PENDING status.
        4. If successful, initiates background sending of emails (one thread per email).
        5. Returns the created Campaign object immediately after DB records are created.
        Handles rollback of Campaign creation if PhishingEmail creation fails.

        Args:
            campaign_name (str): Name of the campaign
            admin_email (str): Email of the admin who started the campaign
            emails (list[str]): List of employee emails to target
            scenario_id (int): ID of the phishing scenario (implies template)

        Returns:
            Campaign: The newly created campaign object.

        Raises:
            ValueError: If validation fails (e.g., invalid scenario, no emails).
            Exception: If database operations fail.
        """

        # Validate recipient emails list
        if not emails:
            raise ValueError("No employee emails provided for campaign")

        # Verify scenario exists and get template
        try:
            template = ScenarioService.get_template_for_scenario(scenario_id)
        except Exception as e:
            raise ValueError(f"Invalid scenario_id {scenario_id}: {str(e)}")

        # 1. Create campaign record
        campaign = None # Initialize campaign to None
        try:
            campaign = CampaignRepository.create_campaign(
                name=campaign_name,
                admin_email=admin_email,
                scenario_id=scenario_id
            )
            print(f"Created Campaign record with ID: {campaign.id}")

            # 2. Create pending PhishingEmail records using PhishingEmailManager
            creation_result = PhishingEmailManager.create_pending_emails(
                campaign_id=campaign.id,
                recipient_emails=emails,
                template_id=template.id
            )

            created_email_ids = creation_result["created_ids"]
            failed_email_creations = creation_result["failed_emails"]

            print(f"Attempted to create PhishingEmail records for campaign {campaign.id}. Success IDs: {len(created_email_ids)}, Failures: {len(failed_email_creations)}.")
            if failed_email_creations:
                print(f"Failed email addresses: {', '.join(failed_email_creations)}")

            # 3. Check if ANY emails were successfully created. If not, abort and clean up.
            if not created_email_ids:
                print(f"No PhishingEmail records were successfully created for campaign {campaign.id}. Rolling back campaign creation.")
                # Attempt to delete the campaign record created earlier
                CampaignRepository.delete_campaign(campaign.id)
                raise ValueError(f"Failed to create any PhishingEmail records for the provided emails.")

            # 4. If we reach here, at least some emails were created. Initiate background sending.
            flask_app = current_app._get_current_object() # Get app context for background tasks
            PhishingEmailManager.start_background_sending(campaign.id, created_email_ids, flask_app)
            print(f"Successfully created campaign {campaign.id} and initiated background email sending.")

            # 5. Return the created campaign object
            return campaign

        except Exception as e:
            print(f"Error during campaign start process: {e}")
            # If campaign object was created before the error, try to clean it up
            if campaign and campaign.id:
                print(f"Attempting to clean up campaign {campaign.id} due to error.")
                try:
                     # Note: Depending on where the error occurred, email records might exist.
                     # We might need a more robust cleanup (e.g., delete associated emails too) or rely on background jobs failing gracefully.
                     # For now, just delete the campaign record itself.
                    CampaignRepository.delete_campaign(campaign.id)
                    print(f"Cleaned up campaign {campaign.id}.")
                except Exception as cleanup_error:
                    print(f"Error during campaign cleanup for {campaign.id}: {cleanup_error}")
            # Re-raise the original exception to signal failure
            raise e

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

