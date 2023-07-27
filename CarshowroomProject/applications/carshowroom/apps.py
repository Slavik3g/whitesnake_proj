from django.apps import AppConfig


class CarshowroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.carshowroom'

    def ready(self):
        from . import signals
        from .models import CarShowroomModel
        signals.post_save.connect(signals.added_showroom, sender=CarShowroomModel)
