from django.conf import settings
from django.utils.module_loading import import_string


def get_push_backend():
    config = getattr(settings, "NOTIFY_HUB_CONFIG", {})
    backend_path = config.get(
        "push_backend",
        "notify_hub.backends.push.fcm_backend.FCMPushNotificationBackend",
    )
    backend_class = import_string(backend_path)
    provider_config = config.get("providers", {}).get("fcm", {})
    return backend_class(**provider_config)


def send_push_notification(token, body, title=None, **kwargs):
    backend = get_push_backend()
    return backend.send_push(token, body, title=title, **kwargs)


def get_sms_backend():
    config = getattr(settings, "NOTIFY_HUB_CONFIG", {})
    backend_path = config.get("sms_backend", "notify_hub.backends.sms.base.SMSBackend")
    backend_class = import_string(backend_path)
    provider_config = config.get("providers", {}).get("sms", {})
    return backend_class(**provider_config)


def send_sms_notification(recipient, body, **kwargs):
    backend = get_sms_backend()
    return backend.send(recipient, body, **kwargs)
