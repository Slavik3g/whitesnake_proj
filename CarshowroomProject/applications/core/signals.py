from django.db.models.signals import post_save
from django.dispatch import receiver

from applications.core.models import BaseUser
from applications.customers.models import CustomerModel


@receiver(post_save, sender=BaseUser)
def create_customer_signal(sender, instance, created, **kwargs):
    if created:
        CustomerModel.objects.create(user=instance)
