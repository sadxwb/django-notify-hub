import abc


class BasePushBackend(abc.ABC):
    def __init__(self, **kwargs):
        self.config = kwargs

    @abc.abstractmethod
    def send_push(self, token, body, title=None, **kwargs):
        pass
