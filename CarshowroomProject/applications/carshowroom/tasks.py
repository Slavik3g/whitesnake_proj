import decimal
from _decimal import Decimal
from datetime import datetime

from celery import shared_task
from django.db.models import Q, Max, Min, F, ExpressionWrapper, Sum
from django.utils import timezone
from rest_framework.fields import DecimalField

from applications.carshowroom.models import CarShowroomModel, CarShowroomCar, CarShowroomSupplierPurchaseHistory
from applications.core.models import CarModel
from applications.customers.models import CustomerPurchaseHistoryModel
from applications.suppliers.models import SupplierCarModel, SupplierDiscount, SupplierModel


# from applications.carshowroom.tasks import *

def max_percent_discount(car, supplier=None, carshowroom=None):
    discounts = SupplierDiscount.objects.filter(
        Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(supplier=supplier)).aggregate(
        Max('percent'))['percent__max']
    return discounts if discounts else 0


def number_of_car_purchases(car, carshowroom):
    return CustomerPurchaseHistoryModel.objects.filter(car=car, carshowroom=carshowroom).count()


def get_individual_supplier_discount(supplier, carshowroom):
    discount = CarShowroomSupplierPurchaseHistory.objects.filter(
        carshowroom=carshowroom, supplier=supplier
    ).aggregate(Sum('cars_count'))['cars_count__sum']
    return discount if discount else 0


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


@shared_task()
def buy_car_from_supplier():
    carshowroomcars = CarShowroomCar.objects.all()
    carshowroomcars = sorted(carshowroomcars,
                             key=lambda x: number_of_car_purchases(car=carshowroomcars.car,
                                                                   carshowroom=carshowroomcars.carshowroom),
                             reverse=True)
    for carshowroomcar in carshowroomcars:
        car = carshowroomcar.car
        supplier = carshowroomcar.supplier
        carshowroom = carshowroomcar.carshowroom

        supplier_car = SupplierCarModel.objects.filter(supplier=supplier, car=car).first()
        if supplier_car:
            individual_discount = get_individual_supplier_discount(carshowroom, supplier)
            discount_price = supplier_car.price * decimal.Decimal(
                (1 - (max_percent_discount(supplier=supplier, car=car) + individual_discount) / 100)
            )
            if carshowroom.balance >= discount_price:
                carshowroom.balance -= Decimal(discount_price)
                supplier.balance += Decimal(discount_price)
                purchase_history = CarShowroomSupplierPurchaseHistory.objects.get_or_create(
                    car=car,
                    supplier=supplier,
                    carshowroom=carshowroom
                )
                purchase_history.cars_count += 1
                purchase_history.total_price += Decimal(discount_price)
                carshowroomcar.number += 1

                carshowroom.save()
                supplier.save()
                purchase_history.save()
                carshowroomcar.save()


