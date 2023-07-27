import json
import random

import pytest

from applications.carshowroom.models import CarShowroomModel
from applications.carshowroom.services import CarshowroomService
from applications.core.enums import CarBrandEnum, CarTypeEnum, CarFuelEnum
from applications.core.models import BaseUser, CarModel
from applications.core.services import UserService, CarService
from applications.suppliers.models import SupplierModel
from applications.suppliers.services import SupplierService

user_service = UserService()
car_service = CarService()
carshowroom_service = CarshowroomService()
supplier_service = SupplierService()


@pytest.fixture
def user():
    user_dc = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password1234',
        'is_confirmed': True
    }

    user = user_service.create_user(user_dc)
    return user


@pytest.fixture
def car():
    car_dc = {
        'brand': random.choice(list(CarBrandEnum)).value,
        'body_type': random.choice(list(CarTypeEnum)).value,
        'fuel': random.choice(list(CarFuelEnum)).value,
        'model': 'TurboV3',
    }

    car = car_service.create_car(car_dc)
    return car


@pytest.fixture
def carshowroom():
    carshowroom_dc = {
        'name': 'TestCarshowroom',
        'country': 'USA',
        'balance': 1000000,
        'car_characteristics': json.dumps({"model": 22315}),
        'discount': 5,
    }

    from applications.carshowroom import signals
    signals.post_save.disconnect(signals.added_showroom, sender=CarShowroomModel)
    carshowroom = carshowroom_service.create_carshowroom(carshowroom_dc)
    signals.post_save.connect(signals.added_showroom, sender=CarShowroomModel)

    return carshowroom



@pytest.fixture
def supplier():
    supplier_dc = {
        'name': 'TestSupplier',
        'created_year': '1990-12-12',
        'discount': 5,
        'count_of_customers': 100,
        'balance': 0
    }

    return supplier_service.create_supplier(supplier_dc)


@pytest.mark.django_db
def test_user_create(user):
    assert BaseUser.objects.count() == 1


@pytest.mark.django_db
def test_car_create(car):
    assert CarModel.objects.count() == 1


@pytest.mark.django_db
def test_carshowroom_create(carshowroom):
    assert CarShowroomModel.objects.count() == 1


@pytest.mark.django_db
def test_supplier_create(supplier):
    assert SupplierModel.objects.count() == 1
