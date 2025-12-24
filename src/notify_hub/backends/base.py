import abc


class BaseBackend(abc.ABC):
    """
    Abstract base class for all notification backends.
    """

    def __init__(self, **kwargs):
        self.config = kwargs

    @abc.abstractmethod
    def send(self, target, body, subject=None, **kwargs):
        """
        Send a notification.

        :param target: The recipient (email, phone number, device token).
        :param body: The content of the notification.
        :param subject: Optional subject for the notification.
        :param kwargs: Additional metadata or provider-specific options.
        :return: (success: bool, error_message: str or None)
        """
        pass
