import decimal
from _decimal import Decimal
from datetime import datetime

from celery import shared_task
from django.db.models import Q, Max, Min, F, ExpressionWrapper, Sum
from django.utils import timezone
from rest_framework.fields import DecimalField

from applications.carshowroom.models import CarShowroomModel, CarShowroomCar, CarShowroomSupplierPurchaseHistory, \
    CarShowroomDiscount
from applications.core.models import CarModel
from applications.customers.models import CustomerPurchaseHistoryModel, OfferModel
from applications.suppliers.models import SupplierCarModel, SupplierDiscount, SupplierModel


# from applications.carshowroom.tasks import *

def max_percent_discount(car, supplier=None, carshowroom=None):
    if supplier is None:
        discounts = CarShowroomDiscount.objects.filter(
            Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(carshowroom=carshowroom)).aggregate(
            Max('percent'))['percent__max']
    else:
        discounts = SupplierDiscount.objects.filter(
            Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(supplier=supplier)).aggregate(
            Max('percent'))['percent__max']
    return discounts if discounts else 0


def number_of_car_purchases(car, carshowroom):
    return CustomerPurchaseHistoryModel.objects.filter(car=car, carshowroom=carshowroom).count()


def get_individual_supplier_discount(carshowroom, supplier):
    discount = CarShowroomSupplierPurchaseHistory.objects.filter(
        carshowroom=carshowroom, supplier=supplier
    ).aggregate(Sum('cars_count'))['cars_count__sum']
    return discount if discount else 0


@shared_task
def confirm_customer(carshowroom_id):
    carshowroom = CarShowroomModel.objects.get(id=carshowroom_id)
    cars = CarModel.objects.filter(**carshowroom.car_characteristics)
    for car in cars:
        supplier_car = SupplierCarModel.objects.filter(car=car).order_by(
            (1 - max_percent_discount(supplier=F('supplier'), car=car) / 100) * F('price')
        ).first()
        if supplier_car:
            CarShowroomCar.objects.get_or_create(
                price=supplier_car.price,
                car=car,
                carshowroom=carshowroom,
                number=0,
                supplier=supplier_car.supplier
            )


@shared_task
def buy_car_from_supplier():
    carshowroomcars = CarShowroomCar.objects.select_related('car').select_related('carshowroom').select_related('supplier').all()
    carshowroomcars = sorted(carshowroomcars,
                             key=lambda x: number_of_car_purchases(car=x.car,
                                                                   carshowroom=x.carshowroom),
                             reverse=True)
    for carshowroomcar in carshowroomcars:
        car = carshowroomcar.car
        supplier = carshowroomcar.supplier
        carshowroom = carshowroomcar.carshowroom

        supplier_car = SupplierCarModel.objects.filter(supplier=supplier, car=car).first()
        if supplier_car:
            individual_discount = get_individual_supplier_discount(carshowroom=carshowroom, supplier=supplier)
            discount_price = supplier_car.price * decimal.Decimal(
                (1 - (max_percent_discount(supplier=supplier, car=car) + individual_discount) / 100)
            )
            if carshowroom.balance >= discount_price:
                carshowroom.balance -= Decimal(discount_price)
                supplier.balance += Decimal(discount_price)
                purchase_history, created = CarShowroomSupplierPurchaseHistory.objects.get_or_create(
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


@shared_task()
def check_suppliers_benefit():
    carshowroomcars = CarShowroomCar.objects.all()
    for carshowroomcar in carshowroomcars:
        supplier_car = SupplierCarModel.objects.filter(car=carshowroomcar.car).order_by(
            (1 - max_percent_discount(supplier=F('supplier'), car=carshowroomcar.car) / 100) * F('price')
        ).first()
        if supplier_car.supplier != carshowroomcar.supplier:
            carshowroomcar.supplier = supplier_car.supplier
            carshowroomcar.save()


@shared_task()
def check_offer():
    offers = OfferModel.objects.select_related('customer').all()
    offers = sorted(offers, key=lambda x: x.updated)
    for offer in offers:
        cars = CarModel.objects.filter(**offer.car_char)
        carshowroom_car = CarShowroomCar.objects.filter(car__in=cars, number__gt=0).order_by(
            (1 - max_percent_discount(carshowroom=F('carshowroom'), car=F('car_model')) / 100 * F('price'))).last()
        if carshowroom_car:
            price = carshowroom_car.price
            if offer.customer.balance >= price and offer.max_price >= price:
                carshowroom_car.carshowroom.balance += Decimal(price)
                offer.customer.balance -= Decimal(price)
                carshowroom_car.number -= 1
                offer.is_active = False
                CustomerPurchaseHistoryModel.objects.create(
                    price=price,
                    carshowroom=carshowroom_car.carshowroom,
                    customer=offer.customer,
                    car=carshowroom_car.car,
                )
                carshowroom_car.save()
                offer.save()
                offer.customer.save()

