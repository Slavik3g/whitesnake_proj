from django.db import models

from CarshowroomProject.apps.carshowroom.models import CarShowroomModel
from CarshowroomProject.apps.core.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.

class CustomerModel(BaseModel):
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    purchase_history = models.ManyToManyField(CarShowroomModel, through='CustomerPurchaseHistoryModel')
    desired_car_characteristic = models.JSONField(default={})

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'


class CustomerPurchaseHistoryModel(BaseModel):
    price = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    car = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'purchase_history'
