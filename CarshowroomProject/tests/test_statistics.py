from _decimal import Decimal

import pytest
from django.db.models import Sum

from applications.carshowroom.models import CarShowroomModel, CarShowroomSupplierPurchaseHistory
from applications.carshowroom.services import CarshowroomService
from applications.core.models import CarModel
from applications.core.services import CarService
from applications.customers.models import CustomerPurchaseHistoryModel, CustomerModel
from applications.customers.services import CustomerService
from applications.suppliers.models import SupplierModel, SupplierCarModel
from applications.suppliers.services import SupplierService

carshowroom_service = CarshowroomService()
customer_service = CustomerService()
supplier_service = SupplierService()
car_service = CarService()


@pytest.fixture
def create_data_customer_purchases(car, carshowroom, customer):
    CustomerPurchaseHistoryModel.objects.create(price=Decimal('500'), carshowroom=carshowroom, customer=customer,
                                                car=car)
    CustomerPurchaseHistoryModel.objects.create(price=Decimal('1000'), carshowroom=carshowroom, customer=customer,
                                                car=car)


@pytest.fixture
def create_data_for_supplier_purchase_history(carshowroom, supplier, car):
    CarShowroomSupplierPurchaseHistory.objects.create(car=car, carshowroom=carshowroom, supplier=supplier,
                                                      total_price=Decimal('1500'), cars_count=2)
    CarShowroomSupplierPurchaseHistory.objects.create(car=car, carshowroom=carshowroom, supplier=supplier,
                                                      total_price=Decimal('2000'), cars_count=3)


@pytest.fixture
def create_supplier_cars(supplier):
    car1_dc = {'brand': 'bmw', 'fuel': 'petrol', 'body_type': 'micro', 'model': 'Test1'}
    car2_dc = {'brand': 'subaru', 'fuel': 'petrol', 'body_type': 'micro', 'model': 'Test2'}
    car1 = car_service.create_car(car1_dc)
    car2 = car_service.create_car(car2_dc)
    SupplierCarModel.objects.create(supplier=supplier, car=car1, price=Decimal('25000'))
    SupplierCarModel.objects.create(supplier=supplier, car=car2, price=Decimal('30000'))


@pytest.mark.django_db
class TestCarShowroomStatistic:
    def test_total_income_money(self, carshowroom, create_data_customer_purchases):
        total_income = carshowroom_service.total_income_money(carshowroom)
        assert total_income == Decimal('1500')

    def test_total_income_money_no_data(self, carshowroom):
        total_income = carshowroom_service.total_income_money(carshowroom)
        assert total_income == 0

    def test_supplier_purchase_history(self, carshowroom, create_data_for_supplier_purchase_history):
        spend_money = carshowroom_service.get_total_spend_money(carshowroom)
        assert spend_money == Decimal('3500')

    def test_supplier_purchase_history_no_data(self, carshowroom):
        spend_money = carshowroom_service.get_total_spend_money(carshowroom)
        assert spend_money == 0

    def test_total_count_of_purchases(self, carshowroom, create_data_customer_purchases):
        total_count_of_purchases = carshowroom_service.total_count_of_purchases(carshowroom)
        assert total_count_of_purchases == 2

    def test_test_total_count_of_purchases_no_data(self, carshowroom):
        total_count_of_purchases = carshowroom_service.total_count_of_purchases(carshowroom)
        assert total_count_of_purchases == 0

    def test_get_statistics_data(self, carshowroom, create_data_customer_purchases,
                                 create_data_for_supplier_purchase_history):
        statistics = carshowroom_service.get_statistics_data(carshowroom)
        assert statistics['total_amount_of_purchases'] == 2
        assert statistics['total_spend_money'] == Decimal('3500')
        assert statistics['total_income_money'] == Decimal('1500')


@pytest.mark.django_db
class TestCustomerStatistic:
    def test_get_customer_cars(self, create_data_customer_purchases, customer, car):
        customer_cars = customer_service.get_customer_cars(customer)
        assert customer_cars[car.brand + " " + car.model] == 2
        assert len(customer_cars) == 1

    def test_get_total_spend_money(self, customer, create_data_customer_purchases):
        total_spend = customer_service.get_total_spend_money(customer)
        assert total_spend == Decimal('1500')

    def test_get_total_spend_money_no_data(self, customer):
        total_spend = customer_service.get_total_spend_money(customer)
        assert total_spend == 0

    def get_statistics_data(self, create_data_customer_purchases, customer, car):
        statistics = customer_service.get_statistics_data(customer)
        assert statistics['total spend money'] == 1500
        assert statistics['customer cars'] == {'lexus TurboV3': 2}


@pytest.mark.django_db
class TestSupplierStatistic:
    def test_get_supplier_cars(self, supplier, create_supplier_cars):
        supplier_cars = supplier_service.get_supplier_cars(supplier)
        assert supplier_cars == [('bmw', 'Test1'), ('subaru', 'Test2')]
