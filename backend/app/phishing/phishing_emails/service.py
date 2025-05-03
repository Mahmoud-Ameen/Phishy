from flask import current_app
import threading
import uuid

# App imports
from app.phishing.phishing_emails.repository import PhishingEmailRepository
from app.phishing.scenarios.repository import TemplateRepository 
from app.phishing.tracking.service import TrackingService
from app.core.mail_service.mail_service import SMTPMailService
from .models import PhishingEmailModel as PhishingEmail
from app.core.exceptions import OperationFailure


class PhishingEmailService:
    """Manages the creation and dispatching of phishing emails for campaigns."""

    @staticmethod
    def process_campaign_emails(campaign_id: int, recipient_emails: list[str], template_id: int, app):
        """
        Creates PhishingEmail records with pre-parsed content and initiates background sending.

        Raises OperationFailure if any record creation fails, 
        allowing the caller (CampaignService) to handle rollback.
        """
        service_name = PhishingEmailService.__name__
        print(f"[{service_name}] Processing {len(recipient_emails)} emails for campaign {campaign_id}...")
        try:
            # Fetch template once before the loop
            template = TemplateRepository.get_template_by_id(template_id)

            # Step 1: Create email records with pre-parsed content 
            # Needs app context for TrackingService URL config
            with app.app_context(): 
                created_ids = PhishingEmailService._create_email_records(
                    campaign_id, 
                    recipient_emails, 
                    template
                )
            print(f"[{service_name}] Successfully created {len(created_ids)} PhishingEmail records for campaign {campaign_id}.")

            # Step 2: Dispatch background sending tasks
            if created_ids:
                # Pass app context needed by the worker for DB access
                PhishingEmailService._dispatch_emails_in_background(campaign_id, created_ids, app)
            else:
                print(f"[{service_name}] No email records created for campaign {campaign_id}. Nothing to dispatch.")

            return created_ids

        except OperationFailure as e: 
            # Handle known failures (template not found, record creation failed)
            print(f"[{service_name}] Email processing failed for campaign {campaign_id}: {e}. Aborting.")
            raise e # Re-raise for CampaignService to handle rollback
        except Exception as e:
            # Handle unexpected errors during the process
            print(f"[{service_name}] Unexpected error processing emails for campaign {campaign_id}: {e}")
            raise OperationFailure(f"Internal error during email processing: {e}") # Wrap unexpected errors

    @staticmethod
    def _create_email_records(campaign_id: int, recipient_emails: list[str], template) -> list[int]:
        """
        Internal: Creates PhishingEmail records with pre-parsed content & tracking UUID.
        Requires Flask app context for config access.
        Raises OperationFailure on first database error.
        """
        created_ids = []
        tracking_url = current_app.config.get('TRACKING_URL', '#') 
        if tracking_url == '#':
            print(f"[WARN] TRACKING_URL not configured in app config. Tracking pixels may not work.")
            
        base_template_content = template.content
        base_subject = template.subject

        for email_address in recipient_emails:
            try:
                # --- Generate UUID and Parse Content --- 
                tracking_uuid = str(uuid.uuid4())
                # Directly use the generated UUID as the tracking key
                tracking_key = tracking_uuid 
                tracking_pixel_url = f"{tracking_url}/{tracking_key}.png"
                
                # Parse content
                final_content = base_template_content
                final_content += f'<img src="{tracking_pixel_url}" alt="" width="1" height="1" style="display:none;visibility:hidden;" />'
                final_content = final_content.replace("{{tracking_key}}", tracking_key) 
                final_subject = base_subject # Assume no placeholders in subject for now

                # --- Create DB Record --- 
                email_record = PhishingEmailRepository.create(
                    recipient_email=email_address,
                    campaign_id=campaign_id,
                    template_id=template.id,
                    tracking_uuid=tracking_uuid, # Pass the generated UUID
                    final_subject=final_subject, 
                    final_content=final_content, 
                    status="pending" 
                )
                created_ids.append(email_record.id)

            except Exception as e:
                print(f"Failed to create PhishingEmail record for {email_address} (Campaign {campaign_id}): {e}. Triggering rollback.")
                raise OperationFailure(f"Failed to create record for {email_address}: {e}")
        return created_ids

    @staticmethod
    def _dispatch_emails_in_background(campaign_id: int, phishing_email_ids: list[int], app):
        """
        Internal: Starts background threads for sending emails.
        """
        print(f"Dispatching background sending for campaign {campaign_id} ({len(phishing_email_ids)} emails)...")
        threads = []
        for email_id in phishing_email_ids:
            # Pass the specific worker function and necessary context
            thread = threading.Thread(target=PhishingEmailService._send_single_email_worker, args=(email_id, app.app_context()))
            thread.daemon = True # Allow main thread to exit
            thread.start()
            threads.append(thread)
        # NOTE: Workers update DB status independently. No need to join threads here.

    @staticmethod
    def _send_single_email_worker(phishing_email_id: int, app_context):
        """
        Internal: Worker function executed in a thread to send one phishing email.
        Uses pre-parsed content stored in the database record.
        """
        log_prefix = f"[Worker-{phishing_email_id}]"
        email_record_model: PhishingEmail | None = None # Use Model for direct field access
        
        with app_context: # Needed for DB access within the thread
            try:
                # --- Step 1: Fetch Record & Validate --- 
                # Fetch the full model to access final_subject/final_content
                # Use PhishingEmailModel directly with SQLAlchemy session from app_context
                email_record_model = PhishingEmail.query.get(phishing_email_id) 
                
                if not email_record_model:
                    print(f"{log_prefix} Error: PhishingEmail record not found.")
                    return
                
                email_address_for_log = email_record_model.recipient_email

                # NOTE: Status should eventually use an Enum
                if email_record_model.status != "pending": # StatusEnum.PENDING
                    print(f"{log_prefix} Info: Email for {email_address_for_log} is not PENDING (Status: {email_record_model.status}). Skipping.")
                    return

                # --- Step 2: Attempt Sending (using pre-parsed content) --- 
                print(f"{log_prefix} Attempting to send email to {email_address_for_log}...")
                # Use the pre-parsed fields from the fetched model
                SMTPMailService.send(
                    email_address_for_log, 
                    email_record_model.final_subject, 
                    email_record_model.final_content  
                )
                
                # Update status to sent upon successful send initiation
                # NOTE: Status should eventually use an Enum
                PhishingEmailRepository.update_status(email_record_model.id, "sent") # StatusEnum.SENT
                print(f"{log_prefix} Successfully sent email to {email_address_for_log} and updated status to SENT.")
                            
            except Exception as setup_error: # Catch errors from Step 1 (fetching record)
                error_details = str(setup_error)

                log_email = email_record_model.recipient_email if email_record_model else "N/A"
                print(f"{log_prefix} Setup error processing email for {log_email}: {error_details}")
                # Update status to failed if we have an email record ID (should always exist if query.get didn't fail)
                if phishing_email_id:
                    try:
                        # NOTE: Status should eventually use an Enum
                        PhishingEmailRepository.update_status(phishing_email_id, "failed", f"Setup Error: {error_details}") # StatusEnum.FAILED
                        print(f"{log_prefix} Updated status to FAILED due to setup error.")
                    except Exception as update_err:
                        # Log critical failure if status update fails
                        print(f"{log_prefix} CRITICAL: Failed to update status to FAILED after setup error: {update_err}")
