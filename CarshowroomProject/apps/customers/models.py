from django.db import models

from apps.carshowroom.models import CarShowroomModel
from apps.core.models import BaseModel, CarModel, BaseUser


class CustomerModel(BaseModel):
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    user = models.OneToOneField(BaseUser, on_delete=models.RESTRICT, primary_key=True)
    purchase_history = models.ManyToManyField(CarShowroomModel, through='CustomerPurchaseHistoryModel')

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.user.username}'


class CustomerPurchaseHistoryModel(BaseModel):
    price = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT)
    car_showroom = models.ForeignKey(CarShowroomModel, on_delete=models.RESTRICT)
    customer = models.ForeignKey(CustomerModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'customer_purchase_history'
        verbose_name = 'CustomerPurchaseHistory'
        verbose_name_plural = 'CustomerPurchaseHistories'

    def __str__(self):
        return f'{self.customer.name} {self.car_showroom.name} {self.car.name} {self.car.model}'
