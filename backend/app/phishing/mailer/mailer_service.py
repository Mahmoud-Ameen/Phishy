from app.phishing.phishing_emails.repository import PhishingEmailRepository
from app.phishing.scenarios.service import ScenarioService
from app.phishing.scenarios.repository import TemplateRepository
from app.phishing.tracking.service import TrackingService
from app.core.mail_service.mail_service import SMTPMailService
from flask import current_app
import threading
# Import PhishingEmail model and status enum
from app.phishing.phishing_emails.models import PhishingEmailModel as PhishingEmail
from time import sleep

class PhishingEmailManager:
    @staticmethod
    def create_pending_emails(campaign_id: int, recipient_emails: list[str], template_id: int):
        """
        Creates PhishingEmail records in the database with PENDING status for a campaign.
        Does NOT send emails.

        Args:
            campaign_id: ID of the campaign
            recipient_emails: List of recipient email addresses
            template_id: ID of the email template to use

        Returns:
            dict: Summary with keys 'created_ids' (list of new PhishingEmail IDs) and 'failed_emails' (list of emails that failed creation)
        """
        created_ids = []
        failed_emails = []

        for email_address in recipient_emails:
            try:
                # TODO: Convert to use enum
                email_record = PhishingEmailRepository.create(
                    recipient_email=email_address,
                    campaign_id=campaign_id,
                    template_id=template_id,
                    status="pending"
                )
                created_ids.append(email_record.id)
            except Exception as e:
                print(f"Failed to create PhishingEmail record for {email_address} in campaign {campaign_id}: {e}")
                failed_emails.append(email_address)

        return {
            "created_ids": created_ids,
            "failed_emails": failed_emails
        }


    @staticmethod
    def start_background_sending(campaign_id: int, phishing_email_ids: list[int], app):
        """
        Starts a background thread for each pending phishing email to send it.

        Args:
            campaign_id: ID of the campaign (for context/logging)
            phishing_email_ids: List of PhishingEmail IDs to process
            app: Flask app context
        """
        print(f"Starting background sending for campaign {campaign_id} for {len(phishing_email_ids)} emails.")
        threads = []
        for email_id in phishing_email_ids:
            thread = threading.Thread(target=PhishingEmailManager._send_single_email_worker, args=(email_id, app.app_context()))
            thread.daemon = True # Allow main thread to exit even if workers are running
            thread.start()
            threads.append(thread)
            print(f"Started worker thread for PhishingEmail ID: {email_id}")
        # Note: We don't necessarily need to join these threads here.
        # They update the DB status independently.

    @staticmethod
    def _send_single_email_worker(phishing_email_id: int, app_context):
        """
        Worker function executed in a separate thread to send a single phishing email.
        Fetches details, sends email, and updates status in DB.

        Args:
            phishing_email_id: ID of the PhishingEmail record to process
            app_context: Flask application context
        """
        with app_context:
            email_record: PhishingEmail | None = None
            sleep(5)
            try:
                # Get the specific email record
                email_record = PhishingEmailRepository.get_by_id(phishing_email_id)
                if not email_record:
                    print(f"[Worker-{phishing_email_id}] Error: PhishingEmail record not found.")
                    return
                # TODO: Update to use enum
                if email_record.status != "pending":
                    print(f"[Worker-{phishing_email_id}] Info: Email is not PENDING (Status: {email_record.status}). Skipping.")
                    return

                # Get template
                template = TemplateRepository.get_template_by_id(email_record.template_id)
                if not template:
                    raise ValueError(f"Template with ID {email_record.template_id} not found for email {phishing_email_id}")

                # Generate tracking key
                tracking_key = TrackingService.generate_tracking_key(email_record.id, email_record.recipient_email)

                # Create tracking pixel URL
                # Ensure SERVER_HOST is configured correctly in Flask app config
                tracking_url = current_app.config.get('TRACKING_URL', 'http://localhost:5000')
                tracking_pixel_url = f"{tracking_url}/{tracking_key}.png"

                # Populate template content
                template_content = template.content
                # Append tracking pixel invisibly
                template_content += f'<img src="{tracking_pixel_url}" alt="" width="1" height="1" style="display:none;visibility:hidden;" />'
                # Replace tracking key placeholder (assuming {{tracking_key}} exists in template)
                template_content = template_content.replace("{{tracking_key}}", tracking_key) # Make sure the key replacement happens *after* pixel addition if needed

                # Send email
                print(f"[Worker-{phishing_email_id}] Sending email to {email_record.recipient_email}...")
                SMTPMailService.send(email_record.recipient_email, template.subject, template_content)

                # Update status to sent
                # TODO: Update to use enum
                PhishingEmailRepository.update_status(email_record.id, "sent")
                print(f"[Worker-{phishing_email_id}] Successfully sent email to {email_record.recipient_email} and updated status to SENT.")

            except Exception as e:
                print(f"[Worker-{phishing_email_id}] Error sending email to {email_record.recipient_email if email_record else 'N/A'}: {e}")
                # Update status to failed if we have an email record ID
                if phishing_email_id:
                    try:
                        # TODO: Update to use enum
                        PhishingEmailRepository.update_status(phishing_email_id, "failed", str(e))
                        print(f"[Worker-{phishing_email_id}] Updated status to FAILED.")
                    except Exception as update_err:
                         print(f"[Worker-{phishing_email_id}] Critical Error: Failed to update status to FAILED after send error: {update_err}")
            # No explicit return needed from thread worker

