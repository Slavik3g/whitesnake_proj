from django.db import models


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CarQuerySet(models.query.QuerySet):
    def get_petrol_cars(self):
        return self.filter(fuel='petrol')



