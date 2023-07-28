from _decimal import Decimal

import pytest
from django.db.models import Sum

from applications.carshowroom.models import CarShowroomModel, CarShowroomSupplierPurchaseHistory
from applications.carshowroom.services import CarshowroomService
from applications.core.models import CarModel
from applications.customers.models import CustomerPurchaseHistoryModel, CustomerModel
from applications.suppliers.models import SupplierModel

carshowroom_service = CarshowroomService()

@pytest.fixture
def create_data_for_total_income(user, carshowroom, car):
    # car_model = CarModel.objects.create(brand='bmw', fuel='petrol', body_type='sedan', model='Camry')
    # car_showroom = CarShowroomModel.objects.create(name='Showroom 1', balance=10000)
    customer = CustomerModel.objects.get(user=user)

    CustomerPurchaseHistoryModel.objects.create(price=Decimal('500'), carshowroom=carshowroom, customer=customer, car=car)
    CustomerPurchaseHistoryModel.objects.create(price=Decimal('1000'), carshowroom=carshowroom, customer=customer, car=car)

@pytest.fixture
def create_data_for_supplier_purchase_history(carshowroom, supplier, car):
    # car_model = CarModel.objects.create(brand='bmw', fuel='petrol', body_type='sedan', model='Camry')
    # car_showroom = CarShowroomModel.objects.create(name='Showroom 1', balance=15000)
    # supplier = SupplierModel.objects.create(name='Supplier 1', created_year='2021-01-01', count_of_customers=5, balance=20000)

    CarShowroomSupplierPurchaseHistory.objects.create(car=car, carshowroom=carshowroom, supplier=supplier, total_price=Decimal('1500'), cars_count=2)
    CarShowroomSupplierPurchaseHistory.objects.create(car=car, carshowroom=carshowroom, supplier=supplier, total_price=Decimal('2000'), cars_count=3)

@pytest.mark.django_db
class TestCarShowroomStatistic:
    def test_total_income_money(self, create_data_for_total_income):
        total_income = carshowroom_service.total_income_money()
        assert total_income == Decimal('1500')

    def test_total_income_money_no_data(self):
        total_income = carshowroom_service.total_income_money()
        assert total_income == 0

    def test_supplier_purchase_history(self, create_data_for_supplier_purchase_history):
        spend_money = carshowroom_service.get_total_spend_money()
        assert spend_money == Decimal('3500')

    def test_supplier_purchase_history_no_data(self):
        spend_money = carshowroom_service.get_total_spend_money()
        assert spend_money == 0
