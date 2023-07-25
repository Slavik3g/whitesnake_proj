from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.core'

    def ready(self):
        from . import signals
        from .models import BaseUser
        signals.post_save.connect(signals.create_customer_signal, sender=BaseUser)
