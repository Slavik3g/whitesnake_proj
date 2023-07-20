from _decimal import Decimal

from celery import shared_task

from apps.carshowroom.models import CarShowroomModel, CarShowroomCar
from apps.core.models import CarModel
from apps.suppliers.models import SupplierCarModel


@shared_task()
def buy_cars_from_suppliers1():
    car_showrooms = CarShowroomModel.objects.all()
    for car_showroom in car_showrooms:
        cars = CarModel.objects.filter(**car_showroom.car_characteristics)
        for car in cars:
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

