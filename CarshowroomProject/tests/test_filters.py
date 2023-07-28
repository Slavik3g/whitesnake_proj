from datetime import date

import pytest

from applications.carshowroom import signals
from applications.carshowroom.filters import CarShowroomFilter
from applications.carshowroom.models import CarShowroomModel
from applications.core.filters import CarFilter
from applications.core.models import CarModel
from applications.suppliers.filters import SupplierFilter
from applications.suppliers.models import SupplierModel


@pytest.fixture
def create_carshowrooms():
    # Create test data using bulk_create
    test_data = [
        CarShowroomModel(country='USA', balance=100000),
        CarShowroomModel(country='Germany', balance=150000),
        CarShowroomModel(country='France', balance=200000),
    ]
    return CarShowroomModel.objects.bulk_create(test_data)


@pytest.fixture
def create_cars():
    # Create test data using bulk_create
    test_data = [
        CarModel(brand='bmw', fuel='petrol', body_type='micro', model='Test1'),
        CarModel(brand='subaru', fuel='petrol', body_type='micro', model='Test2'),
        CarModel(brand='lexus', fuel='diesel', body_type='micro', model='Test3'),
    ]
    return CarModel.objects.bulk_create(test_data)


@pytest.fixture
def create_suppliers():
    # Create test data using bulk_create
    test_data = [
        SupplierModel(created_year=date(2021, 1, 1), balance=100000),
        SupplierModel(created_year=date(2020, 6, 15), balance=150000),
        SupplierModel(created_year=date(2019, 11, 30), balance=200000),
    ]
    return SupplierModel.objects.bulk_create(test_data)


@pytest.mark.django_db
class TestCarShowroomFilter:
    def test_filter_by_country(self, create_carshowrooms):
        filter_params = {'country': 'US'}
        filtered_qs = CarShowroomFilter(filter_params, queryset=CarShowroomModel.objects.all()).qs
        assert filtered_qs.count() == 1
        assert filtered_qs.first().country == 'US'

    def test_filter_by_balance_gte(self, create_carshowrooms):
        qs = CarShowroomModel.objects.all()
        filter_params = {'balance_gte': 150000}
        filtered_qs = CarShowroomFilter(filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2

    def test_filter_by_balance_lte(self, create_carshowrooms):
        qs = CarShowroomModel.objects.all()
        filter_params = {'balance_lte': 150000}
        filtered_qs = CarShowroomFilter(filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2


@pytest.mark.django_db
class TestCarFilter:
    def test_filter_by_brand(self, create_cars):
        qs = CarModel.objects.all()
        print(qs)
        filter_params = {'brand': 'bmw'}
        filtered_qs = CarFilter(filter_params, queryset=qs).qs
        print(filtered_qs)

        assert filtered_qs.count() == 1
        assert filtered_qs.first().brand == 'bmw'

    # Test case for filtering by fuel
    def test_filter_by_fuel(self, create_cars):
        qs = CarModel.objects.all()
        filter_params = {'fuel': 'petrol'}
        filtered_qs = CarFilter(filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2
        assert filtered_qs.first().fuel == 'petrol'

    # Test case for filtering by body_type
    def test_filter_by_body_type(self, create_cars):
        qs = CarModel.objects.all()
        filter_params = {'body_type': 'micro'}
        filtered_qs = CarFilter(filter_params, queryset=qs).qs

        assert filtered_qs.count() == 3
        assert filtered_qs.last().body_type == 'micro'


@pytest.mark.django_db
class TestSupplierFilter:
    def test_filter_by_created_year_gte(self, create_suppliers):
        qs = SupplierModel.objects.all()
        filter_params = {'created_year_gte': date(2020, 1, 1)}
        filtered_qs = SupplierFilter(data=filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2
        assert all(supplier.created_year >= date(2020, 1, 1) for supplier in filtered_qs)

    def test_filter_by_created_year_lte(self, create_suppliers):
        qs = SupplierModel.objects.all()
        filter_params = {'created_year_lte': date(2020, 1, 1)}
        filtered_qs = SupplierFilter(data=filter_params, queryset=qs).qs

        assert filtered_qs.count() == 1
        assert all(supplier.created_year <= date(2020, 1, 1) for supplier in filtered_qs)

    def test_filter_by_balance_gte(self, create_suppliers):
        qs = SupplierModel.objects.all()
        filter_params = {'balance_gte': 150000}
        filtered_qs = SupplierFilter(data=filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2
        assert all(supplier.balance >= 150000 for supplier in filtered_qs)

    def test_filter_by_balance_lte(self, create_suppliers):
        qs = SupplierModel.objects.all()
        filter_params = {'balance_lte': 150000}
        filtered_qs = SupplierFilter(data=filter_params, queryset=qs).qs

        assert filtered_qs.count() == 2
        assert all(supplier.balance <= 150000 for supplier in filtered_qs)
