from django.core.mail.backends.base import BaseEmailBackend
from .o365_backend import O365EmailBackend
from .gmail_backend import GmailBackend
from django.conf import settings


class NotifyHubEmailBackend(BaseEmailBackend):
    """
    Django compatible email backend that routes to O365 or Gmail.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.config = getattr(settings, "NOTIFY_HUB_CONFIG", {})
        self.provider = self.config.get("email_provider", "o365")
        provider_config = self.config.get("providers", {}).get(self.provider, {})

        if self.provider == "o365":
            self.backend = O365EmailBackend(**provider_config)
        elif self.provider == "gmail":
            self.backend = GmailBackend(**provider_config)
        else:
            raise ValueError(f"Unsupported email provider: {self.provider}")

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent_count = 0
        for message in email_messages:
            success, _ = self.backend.send(
                target=message.to[0] if message.to else None,
                body=message.body,
                subject=message.subject,
                from_email=message.from_email,
            )
            if success:
                sent_count += 1
        return sent_count
