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


@pytest.mark.django_db
def test_user_register(client):
    payload = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password1234',
    }
    response = client.post("/api/user/register/", payload, follow=True)
    print(response.data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_register(client):
    payload = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password1234',
    }
    response = client.post("/api/user/register/", payload, follow=True)
    assert response.status_code == 201


@pytest.mark.django_db
def test_carshowroom_register(client):
    payload = {
        'name': 'TestCarshowroom',
        'country': 'RU',
        'balance': 1000000,
        'car_characteristics': json.dumps({"model": 22315}),
        'discount': 5,
    }
    response = client.post("/api/carshowrooms/", payload, follow=True)

    print(response.status_code)
    print(response.content)

    assert response.status_code == 201


@pytest.mark.django_db
def test_car_register(client):
    payload = {
        'brand': 'bmw',
        'body_type': 'sedan',
        'fuel': 'petrol',
        'model': 'X6',
    }
    response = client.post("/api/cars/", payload, follow=True)
    print(response.content)
    assert response.status_code == 201


@pytest.mark.django_db
def test_supplier_register(client):
    payload = {
        'name': 'TestSupplier',
        'created_year': '1990-12-12',
        'discount': 5,
        'count_of_customers': 100,
        'balance': 0
    }
    response = client.post("/api/suppliers/", payload, follow=True)
    assert response.status_code == 201

