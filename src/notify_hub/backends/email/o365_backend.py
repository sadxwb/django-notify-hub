from O365 import Account
from ..base import BaseBackend


class O365EmailBackend(BaseBackend):
    """
    Email backend using Microsoft O365 (via python-o365).
    """

    def send(self, target, body, subject=None, **kwargs):
        try:
            credentials = (
                self.config.get("client_id"),
                self.config.get("client_secret"),
            )
            account = Account(credentials, tenant_id=self.config.get("tenant_id"))

            if not account.is_authenticated:
                # In a real app, you'd handle token or interactive auth
                # For a reusable library, we assume the account is already authenticated or has a token backend
                return False, "O365 Account not authenticated"

            m = account.new_message()
            m.to.add(target)
            m.subject = subject or "Notification"
            m.body = body
            m.send()

            return True, None
        except Exception as e:
            return False, str(e)
