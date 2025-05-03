from flask import current_app
import threading

# App imports
from app.phishing.phishing_emails.repository import PhishingEmailRepository
from app.phishing.scenarios.repository import TemplateRepository 
from app.phishing.tracking.service import TrackingService
from app.core.mail_service.mail_service import SMTPMailService
from .models import PhishingEmailModel as PhishingEmail
from app.core.exceptions import OperationFailure


class PhishingEmailService:

    @staticmethod
    def process_campaign_emails(campaign_id: int, recipient_emails: list[str], template_id: int, app):
        """
        Creates PhishingEmail records and initiates background sending for them.
        Aims for atomicity in record creation - if any record fails, raises an exception.

        Args:
            campaign_id: ID of the campaign
            recipient_emails: List of recipient email addresses
            template_id: ID of the email template to use
            app: Flask app context for background tasks

        Returns:
            List[int]: List of created PhishingEmail IDs if successful.

        Raises:
            OperationFailure: If any email record creation fails.
            Exception: For other unexpected errors.
        """
        print(f"Processing emails for campaign {campaign_id}. Count: {len(recipient_emails)}")
        try:
            # Step 1: Create all email records (atomically within this service's scope)
            created_ids = PhishingEmailService._create_email_records(campaign_id, recipient_emails, template_id)
            print(f"Successfully created {len(created_ids)} PhishingEmail records for campaign {campaign_id}.")

            # Step 2: If creation successful, dispatch emails in the background
            if created_ids:
                PhishingEmailService._dispatch_emails_in_background(campaign_id, created_ids, app)
            else:
                print(f"No email records were created (or needed) for campaign {campaign_id}. Nothing to dispatch.")
                # Not necessarily an error, could be an empty recipient list handled earlier

            return created_ids

        except OperationFailure as e: 
            print(f"Email record creation failed for campaign {campaign_id}: {e}. Aborting processing.")
            raise e # Re-raise the original exception to signal failure
        except Exception as e:
            print(f"Unexpected error during email processing for campaign {campaign_id}: {e}")
            # Wrap unexpected errors
            raise OperationFailure(f"Internal error processing campaign emails: {e}")


    @staticmethod
    def _create_email_records(campaign_id: int, recipient_emails: list[str], template_id: int) -> list[int]:
        """
        Internal method to create PhishingEmail records. Raises OperationFailure on first error.
        
        Returns:
            List[int]: List of created PhishingEmail IDs.
        Raises:
            OperationFailure: If any record creation fails.
        """
        created_ids = []
        # It's generally better to handle transactionality at a higher level or DB level.
        # For now, we raise on first failure as requested by the prompt's rollback requirement.
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
                # On first failure, log, (optionally clean up previously created IDs if needed/possible),
                # and raise a specific exception to signal failure to the caller.
                print(f"Failed to create PhishingEmail record for {email_address} in campaign {campaign_id}: {e}. Triggering rollback.")
                # Optional: Add cleanup logic here if necessary
                # for created_id in created_ids:
                #    try: PhishingEmailRepository.delete(created_id) # Requires a delete method
                #    except: pass # Best effort cleanup
                raise OperationFailure(f"Failed to create record for {email_address}: {e}")

        return created_ids


    @staticmethod
    def _dispatch_emails_in_background(campaign_id: int, phishing_email_ids: list[int], app):
        """
        Internal method to start background threads for sending emails.
        """
        print(f"Dispatching background sending for campaign {campaign_id} for {len(phishing_email_ids)} emails.")
        threads = []
        for email_id in phishing_email_ids:
            # Pass the service method itself
            thread = threading.Thread(target=PhishingEmailService._send_single_email_worker, args=(email_id, app.app_context()))
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
            # Optional: add a small delay if needed, e.g., sleep(1)
            # sleep(5) # Consider if this fixed delay is necessary
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
                    # Log error and update status to failed
                    error_msg = f"Template with ID {email_record.template_id} not found for email {phishing_email_id}"
                    print(f"[Worker-{phishing_email_id}] Error: {error_msg}")
                    PhishingEmailRepository.update_status(phishing_email_id, "failed", error_msg)
                    print(f"[Worker-{phishing_email_id}] Updated status to FAILED due to missing template.")
                    return # Stop processing this email

                # Generate tracking key
                tracking_key = TrackingService.generate_tracking_key(email_record.id, email_record.recipient_email)

                # Create tracking pixel URL
                # Ensure TRACKING_URL is configured correctly in Flask app config
                tracking_url = current_app.config.get('TRACKING_URL') 
                if not tracking_url:
                     print(f"[Worker-{phishing_email_id}] Warning: TRACKING_URL not configured in Flask app. Tracking pixel might not work.")
                     tracking_pixel_url = "#" # Default to a non-functional URL
                else:
                    tracking_pixel_url = f"{tracking_url}/{tracking_key}.png"


                # Populate template content
                template_content = template.content
                # Append tracking pixel invisibly
                template_content += f'<img src="{tracking_pixel_url}" alt="" width="1" height="1" style="display:none;visibility:hidden;" />'
                # Replace tracking key placeholder (assuming {{tracking_key}} exists in template)
                # Consider making the placeholder configurable
                template_content = template_content.replace("{{tracking_key}}", tracking_key) 

                # Send email
                print(f"[Worker-{phishing_email_id}] Sending email to {email_record.recipient_email}...")
                SMTPMailService.send(email_record.recipient_email, template.subject, template_content)

                # Update status to sent
                # TODO: Update to use enum
                PhishingEmailRepository.update_status(email_record.id, "sent")
                print(f"[Worker-{phishing_email_id}] Successfully sent email to {email_record.recipient_email} and updated status to SENT.")

            except Exception as e:
                error_details = str(e)
                print(f"[Worker-{phishing_email_id}] Error sending email to {email_record.recipient_email if email_record else 'N/A'}: {error_details}")
                # Update status to failed if we have an email record ID
                if phishing_email_id:
                    try:
                        # TODO: Update to use enum
                        PhishingEmailRepository.update_status(phishing_email_id, "failed", error_details)
                        print(f"[Worker-{phishing_email_id}] Updated status to FAILED.")
                    except Exception as update_err:
                         print(f"[Worker-{phishing_email_id}] Critical Error: Failed to update status to FAILED after send error: {update_err}")
            # No explicit return needed from thread worker 