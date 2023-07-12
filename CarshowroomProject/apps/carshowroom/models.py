from django.db import models
from CarshowroomProject.apps.core.models import BaseModel, CarModel
from django_countries.fields import CountryField


class CarShowroomModel(BaseModel):
    name = models.CharField(max_length=100)
    country = CountryField()
    unique_customers = models.ForeignKey('UniqueCarShowroomCustomer', on_delete=models.CASCADE)
    car_characteristics = models.JSONField()
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    class Meta:
        db = 'carshowroom'


class UniqueCarShowroomCustomerModel(BaseModel):
    number_purchases = models.PositiveIntegerField(default=0)


class CarShowroomHistory(BaseModel):
    pass
