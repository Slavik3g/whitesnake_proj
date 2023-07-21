from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.core.models import BaseModel, CarModel, BaseDiscountModel
from applications.suppliers.models import SupplierModel


class CarShowroomModel(BaseModel):
    name = models.CharField(max_length=100)
    country = CountryField(default='US')
    car_characteristics = models.JSONField(default=dict)
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    car_list = models.ManyToManyField(CarModel, through='CarShowroomCar')

    class Meta:
        db_table = 'carshowroom'
        verbose_name = 'CarShowroom'
        verbose_name_plural = 'CarShowrooms'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.country}'


class CarShowroomCar(BaseModel):
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT)
    car_showroom = models.ForeignKey(CarShowroomModel, on_delete=models.RESTRICT)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'car_showroom_car'
        verbose_name = 'CarShowroomCar'
        verbose_name_plural = 'CarShowroomsCars'

    def __str__(self):
        return f'{self.car_showroom.name} {self.car.name} {self.car.model}'


class CarShowroomDiscount(BaseModel, BaseDiscountModel):
    car_showroom = models.ForeignKey(CarShowroomModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'car_showroom_discount'
        verbose_name = 'CarShowroomDiscount'
        verbose_name_plural = 'CarShowroomsDiscounts'
        ordering = ['discount_start']

    def __str__(self):
        return f'{self.car_showroom.name} {self.car_model.name} {self.car_model.model}'


class CarShowroomSupplierPurchaseHistory(BaseModel):
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT)
    carshowroom = models.ForeignKey(CarShowroomModel, on_delete=models.RESTRICT)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.RESTRICT)
    total_price = models.DecimalField(default=0, max_digits=14, decimal_places=2)
    cars_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'car_showroom_purchase_history'
        verbose_name = 'CarShowroomSupplierPurchaseHistory'
        verbose_name_plural = 'CarShowroomSupplierPurchaseHistories'

    def __str__(self):
        return f'{self.carshowroom.name} {self.supplier.name} {self.car.name} {self.car.model}'
