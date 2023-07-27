from django.db.models.signals import post_save
from django.dispatch import receiver

from applications.carshowroom.models import CarShowroomModel
from .tasks import confirm_customer


@receiver(post_save, sender=CarShowroomModel)
def added_showroom(sender, created, instance, **kwargs):
    if created:
        confirm_customer.delay(instance.id)
