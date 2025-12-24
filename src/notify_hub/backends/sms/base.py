from ..base import BaseBackend


class SMSBackend(BaseBackend):
    """
    Base SMS backend. Providers to be implemented.
    """

    def send(self, target, body, subject=None, **kwargs):
        # Placeholder for SMS providers like Twilio, MessageBird, etc.
        # For now, it just logs or does nothing.
        print(f"SMS would be sent to {target}: {body}")
        return True, None
