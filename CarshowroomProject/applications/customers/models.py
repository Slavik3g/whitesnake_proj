from django.db import models

from applications.carshowroom.models import CarShowroomModel
from applications.core.models import BaseModel, CarModel, BaseUser


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
    carshowroom = models.ForeignKey(CarShowroomModel, on_delete=models.RESTRICT)
    customer = models.ForeignKey(CustomerModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'customer_purchase_history'
        verbose_name = 'CustomerPurchaseHistory'
        verbose_name_plural = 'CustomerPurchaseHistories'

    def __str__(self):
        return f'{self.customer.name} {self.carshowroom.name} {self.car.name} {self.car.model}'


class OfferModel(BaseModel):
    customer = models.ForeignKey(CustomerModel, on_delete=models.RESTRICT)
    max_price = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    car_char = models.JSONField()

    class Meta:
        db_table = 'customer_offer'
        verbose_name = 'CustomerOffer'
        verbose_name_plural = 'CustomersOffers'
        ordering = ('created',)