from firebase_admin import messaging, credentials, initialize_app, get_app
from .base import BasePushBackend


class FCMPushNotificationBackend(BasePushBackend):
    """
    Push notification backend using Firebase Cloud Messaging (FCM).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            get_app()
        except ValueError:
            cert = self.config.get("credential_path")
            if cert:
                cred = credentials.Certificate(cert)
                initialize_app(cred)

    def send_push(self, token, body, title=None, **kwargs):
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title or "Notification",
                    body=body,
                ),
                token=token,
                data=kwargs.get("data"),
            )
            messaging.send(message)
            return True, None
        except Exception as e:
            return False, str(e)

    def send(self, target, body, subject=None, **kwargs):
        return self.send_push(target, body, title=subject, **kwargs)
