from _decimal import Decimal
from datetime import datetime

from celery import shared_task
from django.db.models import Q

from applications.carshowroom.models import CarShowroomModel, CarShowroomCar
from applications.core.models import CarModel
from applications.suppliers.models import SupplierCarModel, SupplierDiscount


# from applications.carshowroom.tasks import *
def buy_cars_from_suppliers1():
    car_showrooms = CarShowroomModel.objects.all()
    for car_showroom in car_showrooms:
        cars = CarModel.objects.filter(**car_showroom.car_characteristics)
        for car in cars:
            discounts = SupplierDiscount.objects.filter(Q(car=car) & Q('discount_end' < datetime.now().date()))
            supplier_car = SupplierCarModel.objects.filter(car=car).order_by('price').first()
            if supplier_car:
                print(car_showroom.name, car_showroom.car_characteristics, supplier_car.price)
                print(supplier_car.supplier.balance)
                if car_showroom.balance >= supplier_car.price:
                    car_showroom.balance -= supplier_car.price
                    supplier_car.supplier.balance += supplier_car.price
                    CarShowroomCar.objects.get_or_create(
                        car=car,
                        car_showroom=car_showroom,
                        price=(supplier_car.price + Decimal(0.1) * supplier_car.price),
                        number=1,
                    )

