from django.conf import settings
from django.utils import timezone
from .models import Notification
from .backends.email.o365_backend import O365EmailBackend
from .backends.email.gmail_backend import GmailBackend
from .backends.push.fcm_backend import FCMBackend
from .backends.sms.base import SMSBackend


class NotifyHub:
    """
    Central hub for dispatching notifications.
    """

    def __init__(self):
        self.config = getattr(settings, "NOTIFY_HUB_CONFIG", {})
        self.backends = {
            "o365": O365EmailBackend,
            "gmail": GmailBackend,
            "fcm": FCMBackend,
            "sms": SMSBackend,
        }

    def send_notification(
        self, channel, provider, target, body, subject=None, **kwargs
    ):
        """
        Send a notification and track it in the database.
        """
        # Create notification record
        notification = Notification.objects.create(
            channel=channel,
            provider=provider,
            target=target,
            subject=subject or "",
            body=body,
            status="pending",
        )

        backend_class = self.backends.get(provider)
        if not backend_class:
            notification.status = "failed"
            notification.error_message = f"Provider {provider} not supported"
            notification.save()
            return False, notification.error_message

        # Get provider specific config from settings
        provider_config = self.config.get("providers", {}).get(provider, {})
        backend = backend_class(**provider_config)

        success, error = backend.send(target, body, subject=subject, **kwargs)

        if success:
            notification.status = "sent"
            notification.sent_at = timezone.now()
        else:
            notification.status = "failed"
            notification.error_message = error

        notification.save()
        return success, error


notify_hub = NotifyHub()
