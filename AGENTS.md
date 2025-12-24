# AGENTS.md - AI Agent Documentation

This file provides instructions for AI agents on how to use, extend, and maintain the `django-notify-hub` project.

## Project Structure

- `src/notify_hub/`: Core app directory.
- `src/notify_hub/backends/`: Individual channel implementations.
- `src/notify_hub/models.py`: Database schema for tracking notifications.
- `src/notify_hub/hub.py`: The main entry point for sending notifications.

## Extension Guide

### Adding a New Provider

1.  **Create a new backend**: Inherit from `BaseBackend` in `src/notify_hub/backends/base.py`.
2.  **Implement the `send` method**: Follow the signature `send(target, body, subject=None, **kwargs)`.
3.  **Register the backend**: Add the new backend class to the `self.backends` dictionary in `NotifyHub.__init__` within `src/notify_hub/hub.py`.
4.  **Update Config Expectations**: Document any new configuration keys needed in `settings.py`.

### Modifying the Schema

If you need to store more metadata about notifications, update `src/notify_hub/models.py` and run:
```bash
python manage.py makemigrations notify_hub
```

## Common Tasks for Agents

- **Debugging**: Check `Notification` records for `error_message`.
- **Testing**: Use mock backends for unit tests to avoid sending real notifications.
- **Refactoring**: Ensure all backends continue to return `(bool, str|None)`.
