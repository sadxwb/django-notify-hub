import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from ..base import BaseBackend


class GmailBackend(BaseBackend):
    """
    Email backend using Google Gmail API.
    """

    def send(self, target, body, subject=None, **kwargs):
        try:
            # Assumes service account or OAuth2 credentials provided in config
            creds = self.config.get("credentials")
            service = build("gmail", "v1", credentials=creds)

            message = EmailMessage()
            message.set_content(body)
            message["To"] = target
            message["From"] = self.config.get("from_email")
            message["Subject"] = subject or "Notification"

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            service.users().messages().send(userId="me", body=create_message).execute()

            return True, None
        except Exception as e:
            return False, str(e)
