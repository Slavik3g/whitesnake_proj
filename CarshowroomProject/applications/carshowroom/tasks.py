from _decimal import Decimal
from datetime import datetime

from celery import shared_task
from django.db.models import Q, Max, Min, F, ExpressionWrapper, Sum
from django.utils import timezone
from rest_framework.fields import DecimalField

from applications.carshowroom.models import CarShowroomModel, CarShowroomCar, CarShowroomSupplierPurchaseHistory
from applications.core.models import CarModel
from applications.suppliers.models import SupplierCarModel, SupplierDiscount, SupplierModel


# from applications.carshowroom.tasks import *

def max_percent_discount(car, supplier=None, carshowroom=None):
    discounts = SupplierDiscount.objects.filter(
        Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(supplier=supplier)).aggregate(
        Max('percent'))['percent__max']
    return discounts if discounts else 0


def max_count_for_bonus(supplier, carshowroom):
    disc = CarShowroomSupplierPurchaseHistory.objects.filter(
        carshowroom=carshowroom, supplier=supplier, is_active=True
    ).aggregate(Sum('number_of_purchases'))['number_of_purchases__sum']
    return disc if disc else 0

@shared_task()
def confirm_customers():
    car_showrooms = CarShowroomModel.objects.all()
    for car_showroom in car_showrooms:
        cars = CarModel.objects.filter(**car_showroom.car_characteristics)
        for car in cars:
            supplier_car = SupplierCarModel.objects.filter(car=car).order_by(
                (1 - max_percent_discount(car=car, supplier=F('supplier')) / 100) * F('price')
            ).first()
            if supplier_car:
                CarShowroomCar.objects.get_or_create(
                    car=car,
                    car_showroom=car_showroom,
                    price=supplier_car.price,
                    number=0,
                    supplier=supplier_car.supplier
                )


# @shared_task()
# def buy_car_from_supplier():
#     if car_showroom.balance >= supplier_car.price:
#         car_showroom.balance -= supplier_car.price
#         supplier_car.supplier.balance += supplier_car.price
