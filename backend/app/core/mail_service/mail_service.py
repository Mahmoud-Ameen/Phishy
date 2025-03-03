import os
from abc import ABC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from typing import Literal

# Load environment variables
load_dotenv()

ContentType = Literal['plain', 'html']

class MailService(ABC):
    """Interface for sending emails."""
    @staticmethod
    def send(to: str, subject: str, body: str, content_type: ContentType = 'html'):
        pass


class SMTPMailService(MailService):
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('MAIL_PORT', '587'))

    @staticmethod
    def send(to: str, subject: str, body: str, content_type: ContentType = 'html'):
        if not all([SMTPMailService.username, SMTPMailService.password]):
            raise ValueError("Mail credentials not configured. Check your .env file.")
            
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTPMailService.username
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, content_type))

        with smtplib.SMTP(SMTPMailService.smtp_server, SMTPMailService.smtp_port) as server:
            server.starttls()
            server.login(SMTPMailService.username, SMTPMailService.password)
            server.sendmail(SMTPMailService.username, to, msg.as_string())


