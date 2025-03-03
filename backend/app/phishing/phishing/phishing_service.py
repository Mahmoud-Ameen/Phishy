from ..phishing_emails.repository import PhishingEmailRepository
from ..templates.service import TemplateService
from ...core.mail_service.mail_service import SMTPMailService  # Note: This can be done using dependency injection


class PhishingService:
    @staticmethod
    def send_phishing_email(to: str, template_id: int, campaign_id: int):
        """
        Raises:
            TemplateDoesntExist if the template is not found
        """ ""

        # Get template
        template = TemplateService.get_template_by_id(template_id)

        # Save email to database and use the id as the tracking key
        email = PhishingEmailRepository.create(recipient_email=to, campaign_id=campaign_id, template_id=template.id)
        tracking_key = email.id

        # populate template with tracking key
        click_link = f"http://localhost:3000/phishing/click/{tracking_key}"
        open_link = f"http://localhost:3000/phishing/openmail/{tracking_key}"
        template.content = template.content.replace("[[[click-link]]]", click_link)
        template.content = template.content.replace("[[[open-link]]]", open_link)

        # Send email
        print(f"Sending email{email.id}... to {to} with template {template.id}: {template.subject} \n {template.content}")
        SMTPMailService.send(to, template.subject, template.content)
        print(f"Sent phishing email...")

        pass

    @staticmethod
    def send_phishing_emails(to: list[str], template_id: int, campaign_id: int):
        """
        Send phishing emails to multiple recipients
        """
        for recipient in to:
            PhishingService.send_phishing_email(recipient, template_id, campaign_id)
