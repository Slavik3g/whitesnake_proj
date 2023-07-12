from django.db import models
import enums


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CarModel(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=30, choices=enums.CarBrandEnum.choices())
    fuel = models.CharField(max_length=30, choices=enums.CarFuelEnum.choices())
    type = models.CharField(max_length=30, choices=enums.CarTypeEnum.choices())
    model = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        db_table = 'car'

