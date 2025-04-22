from app.phishing.phishing_emails.repository import PhishingEmailRepository
from app.phishing.scenarios.service import TemplateService
from app.phishing.tracking.service import TrackingService
from app.core.mail_service.mail_service import SMTPMailService
from flask import current_app
import threading


class PhishingService:
    @staticmethod
    def send_phishing_email(to: str, template_id: int, campaign_id: int):
        """
        Send a phishing email to a target
        Args:
            to: Recipient email address
            template_id: ID of the email template to use
            campaign_id: ID of the campaign this email belongs to
        Returns:
            PhishingEmail: The created phishing email record
        Raises:
            TemplateDoesntExist if the template is not found
        """
        # Get template
        template = TemplateService.get_template_by_id(template_id)

        # Create phishing email record with pending status
        email = PhishingEmailRepository.create(
            recipient_email=to,
            campaign_id=campaign_id,
            template_id=template_id
        )

        try:
            # Generate tracking key
            tracking_key = TrackingService.generate_tracking_key(email.id, to)

            # Create tracking pixel URL
            tracking_pixel_url = f"{current_app.config['SERVER_HOST']}/api/tracking/open/{tracking_key}"

            # Populate template with tracking key and pixel
            template_content : str = template.content
            template_content += f'<img src="{tracking_pixel_url}" alt="" width="1" height="1" style="display:none" />'
            template_content = template.content.replace("{{tracking_key}}", tracking_key)

            # Send email
            SMTPMailService.send(to, template.subject, template_content)

            # Update status to sent
            email = PhishingEmailRepository.update_status(email.id, "sent")
            return email

        except Exception as e:
            # Update status to failed
            PhishingEmailRepository.update_status(email.id, "failed", str(e))
            raise e

    @staticmethod
    def send_phishing_emails(to: list[str], template_id: int, campaign_id: int):
        """
        Send phishing emails to multiple recipients
        Args:
            to: List of recipient email addresses
            template_id: ID of the email template to use
            campaign_id: ID of the campaign these emails belong to
        Returns:
            list[PhishingEmail]: List of created phishing email records
        """
        results = []
        for recipient in to:
            try:
                email = PhishingService.send_phishing_email(recipient, template_id, campaign_id)
                results.append(email)
            except Exception as e:
                # Log error but continue with other recipients
                print(f"Failed to send email to {recipient}: {str(e)}")
                continue
        return results

    @staticmethod
    def process_campaign_emails_in_background(campaign_id: int, scenario_id: int):
        """
        Process all pending emails for a campaign in a background thread.
        Args:
            campaign_id: ID of the campaign
            scenario_id: ID of the scenario/template to use
        """
        # Capture the app instance from the current context before spawning the thread
        app = current_app._get_current_object()
        
        def _process_emails():
            print(f"Starting email send task for campaign {campaign_id}")
            success_count = 0
            
            # Use the captured app instance instead of the proxy
            with app.app_context():
                pending_emails = PhishingEmailRepository.get_by_campaign_id(campaign_id)
                pending_emails = [email for email in pending_emails if email.status == "pending"]
                
                print(f"Found {len(pending_emails)} pending emails for campaign {campaign_id}")
                
                for email in pending_emails:
                    try:
                        PhishingService.send_phishing_email(email.recipient_email, scenario_id, campaign_id)
                        success_count += 1
                        print(f"Successfully processed email to {email.recipient_email} for campaign {campaign_id}")
                    except Exception as e:
                        print(f"Failed processing email to {email.recipient_email} for campaign {campaign_id}: {str(e)}")
                        continue
                
                print(f"Finished email send task for campaign {campaign_id}. Processed {success_count}/{len(pending_emails)} emails successfully.")
        
        thread = threading.Thread(
            target=_process_emails,
            daemon=True
        )
        thread.start()
        return thread
