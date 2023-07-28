import json

import pytest
from django.contrib.auth.hashers import make_password, check_password
from pytest_lazyfixture import lazy_fixture
from django.forms.models import model_to_dict

from applications.core.services import UserService


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/cars/', lazy_fixture('car')),
        ('/api/carshowrooms/', lazy_fixture('carshowroom')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_create_entity(url, entity, client):
    response = client.post(url, model_to_dict(entity))
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/user/', lazy_fixture('user')),
        ('/api/cars/', lazy_fixture('car')),
        ('/api/carshowrooms/', lazy_fixture('carshowroom')),
        ('/api/customers/', lazy_fixture('user')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_get_entity(url, entity, client):
    response = client.get(url + str(entity.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    ['/api/user/', '/api/cars/', '/api/carshowrooms/', '/api/customers/', '/api/suppliers/'])
def test_get_list(url, client):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_register(client):
    user_dc = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password'
    }
    response = client.post('/api/user/register/', user_dc)
    assert response.status_code == 201


@pytest.mark.django_db
def test_email_send(client, user):
    email_dc = {
        'email': 'testemail@gmail.com'
    }
    response = client.post('/api/reset_password/', email_dc, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_email_confirm(db, client, user):
    password_dc = {
        'new_password': 'new_pass123'
    }
    user_service = UserService()
    uidb64 = user_service.create_uidb64(user.id)
    token = user_service.get_tokens_for_user(user=user)['access']
    response = client.post(f'/api/reset_password/confirm/{uidb64}/{token}', password_dc, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_email_confirm(db, user, client):
    user_service = UserService()
    token = user_service.get_tokens_for_user(user=user)['access']
    uidb64 = user_service.create_uidb64(user.pk)
    password_data = {
        'new_password': 'new_pass123'
    }
    response = client.post(f'/api/reset_password/confirm/{uidb64}/{token}/', password_data, follow=True, format='json')

    assert response.status_code == 200
    assert response.data == {'detail': 'Password reset successful.'}
    user.refresh_from_db()
    assert check_password('new_pass123', user.password) is True
