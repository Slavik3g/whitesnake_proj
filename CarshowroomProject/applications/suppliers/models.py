from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.core.models import BaseModel, CarModel, BaseDiscountModel


# Create your models here

class SupplierModel(BaseModel):
    name = models.CharField(max_length=100)
    created_year = models.DateField()
    count_of_customers = models.PositiveIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cars_list = models.ManyToManyField(CarModel, through='SupplierCarModel')
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'supplier'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class SupplierCarModel(BaseModel):
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.RESTRICT)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'supplier_car'
        verbose_name = 'SupplierCar'
        verbose_name_plural = 'SupplierCars'

    def __str__(self):
        return f'{self.supplier.name} {self.car.brand} {self.car.model}'


class SupplierDiscount(BaseModel, BaseDiscountModel):
    supplier = models.ForeignKey(SupplierModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'supplier_discount'
        verbose_name = 'SupplierDiscount'
        verbose_name_plural = 'SupplierDiscounts'
        ordering = ['discount_start']

    def __str__(self):
        return f'{self.supplier.name} {self.car_model.name} {self.car_model.model}'

