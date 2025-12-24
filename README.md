# Django Notify Hub

A reusable Django app for unified notifications across multiple channels: Email (O365, Gmail), SMS, and Push (FCM).

## Features

- **Email Backends**: 
    - Office 365 (via `python-o365`)
    - Gmail (via Google APIs)
- **Push Notifications**:
    - Firebase Cloud Messaging (FCM)
- **SMS**:
    - Extensible base for SMS providers.
- **Notification Tracking**: 
    - Database-backed logging of all sent notifications.

## Installation

```bash
pip install django-notify-hub
```

Add `notify_hub` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'notify_hub',
]
```

## Integration with Django Email

To use Notify Hub as your primary email backend, update `EMAIL_BACKEND` in your `settings.py`:

```python
EMAIL_BACKEND = 'notify_hub.backends.email.django_backend.NotifyHubEmailBackend'

NOTIFY_HUB_CONFIG = {
    'email_provider': 'o365', # or 'gmail'
    'providers': {
        ...
    }
}
```

Now, standard Django `send_mail` will use Notify Hub:

```python
from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

## Standard Notification Wrappers

Notify Hub provides standard wrappers for Push and SMS notifications, similar to Django's `send_mail`.

### Push Notifications

```python
from notify_hub.utils import send_push_notification

send_push_notification(
    token='device-token',
    body='Your order is ready!',
    title='Order Update'
)
```

### SMS Notifications

```python
from notify_hub.utils import send_sms_notification

send_sms_notification(
    recipient='+1234567890',
    body='Your verification code is 123456'
)
```

## Configuration

Add `NOTIFY_HUB_CONFIG` to your `settings.py`:

```python
NOTIFY_HUB_CONFIG = {
    'email_provider': 'o365',
    'push_backend': 'notify_hub.backends.push.fcm_backend.FCMPushNotificationBackend',
    'sms_backend': 'notify_hub.backends.sms.base.SMSBackend',
    'providers': {
        'o365': {
            'client_id': 'your-client-id',
            'client_secret': 'your-client-secret',
            'tenant_id': 'your-tenant-id',
        },
        'fcm': {
            'credential_path': 'path/to/firebase-sdk.json',
        },
        ...
    }
}
```

## Usage

```python
from notify_hub.hub import notify_hub

# Send an email via O365
notify_hub.send_notification(
    channel='email',
    provider='o365',
    target='user@example.com',
    subject='Hello',
    body='General Kenobi!'
)

# Send a push notification
notify_hub.send_notification(
    channel='push',
    provider='fcm',
    target='device-registration-token',
    subject='Alert',
    body='System update available'
)
```

## Tracking

You can view the status of notifications in the Django Admin or by querying the `Notification` model:

```python
from notify_hub.models import Notification

failed_notifications = Notification.objects.filter(status='failed')
```
