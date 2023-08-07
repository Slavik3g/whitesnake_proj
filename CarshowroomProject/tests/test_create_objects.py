import json

import pytest

from applications.carshowroom import signals
from applications.carshowroom.filters import CarShowroomFilter
from applications.carshowroom.models import CarShowroomModel
from applications.core.models import BaseUser, CarModel
from applications.suppliers.models import SupplierModel


@pytest.mark.django_db
def test_user_create(new_user1):
    assert BaseUser.objects.get(id=1).username == "TestUser"


@pytest.mark.django_db
def test_car_create(car):
    assert CarModel.objects.count() == 1


@pytest.mark.django_db
def test_carshowroom_create(carshowroom):
    assert CarShowroomModel.objects.count() == 1


@pytest.mark.django_db
def test_supplier_create(supplier):
    assert SupplierModel.objects.count() == 1


