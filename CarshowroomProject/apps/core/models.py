from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.enums import CarBrandEnum, CarFuelEnum, CarTypeEnum


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def safe_delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class CarModel(BaseModel):
    brand = models.CharField(max_length=30, choices=CarBrandEnum.choices())
    fuel = models.CharField(max_length=30, choices=CarFuelEnum.choices())
    body_type = models.CharField(max_length=30, choices=CarTypeEnum.choices())
    model = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        db_table = 'car'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['brand', 'model']


class BaseUser(AbstractUser):
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'


class BaseDiscountModel(models.Model):
    percent = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    car_model = models.ManyToManyField(CarModel)
    discount_start = models.DateField()
    discount_end = models.DateField()
    description = models.CharField(max_length=500, null=True)

    class Meta:
        abstract = True
