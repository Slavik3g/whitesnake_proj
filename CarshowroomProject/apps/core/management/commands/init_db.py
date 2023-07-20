import random
import string
from datetime import datetime, timedelta
from enum import Enum

from django.core.management.base import BaseCommand
from django.db.models import Min, Max

from apps.core.models import CarModel
from apps.core.enums import CarBrandEnum, CarFuelEnum, CarTypeEnum
from apps.carshowroom.models import CarShowroomModel
from django_countries import countries

from apps.suppliers.models import SupplierModel, SupplierCarModel


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        self._create_cars()
        self._create_showrooms()
        self._create_suppliers()
        self._create_suppliers_cars()

    def _create_suppliers(self):
        if SupplierModel.objects.count() >= 10:
            return
        for i in range(10):
            random_date = self._generate_random_date(datetime(1990, 1, 1), datetime.now())
            SupplierModel.objects.get_or_create(
                name=self._generate_random_string(random.randint(4, 10)),
                created_year=random_date,
                discount=random.randint(0, 10),
                count_of_customers=random.randint(20, 500),
                balance=random.randint(10_000, 1_000_000),
            )

    def _create_suppliers_cars(self):
        if SupplierCarModel.objects.count() >= 40:
            return
        for i in range(40):
            SupplierCarModel.objects.get_or_create(
                supplier=SupplierModel.objects.get(id=random.randint(
                    SupplierModel.objects.aggregate(Min('id'))['id__min'],
                    SupplierModel.objects.aggregate(Max('id'))['id__max']
                )),
                car=CarModel.objects.get(id=random.randint(
                    CarModel.objects.aggregate(Min('id'))['id__min'],
                    CarModel.objects.aggregate(Max('id'))['id__max']
                )),
                price=random.randint(10_000, 200_000),
            )

    def _create_cars(self):
        if CarModel.objects.count() >= 20:
            return
        for _ in range(20):
            CarModel.objects.get_or_create(
                brand=random.choice(list(CarBrandEnum)).value,
                fuel=random.choice(list(CarFuelEnum)).value,
                body_type=random.choice(list(CarTypeEnum)).value,
                model=self._generate_random_string(5),
            )

    def _create_showrooms(self):
        if CarShowroomModel.objects.count() >= 10:
            return
        for _ in range(10):
            characteristic1 = random.choice(list(self.CarCharacteristics))
            characteristic2 = random.choice(list(self.CarCharacteristics))
            CarShowroomModel.objects.get_or_create(
                name=self._generate_random_string(random.randint(4, 10)),
                country=random.choice(list(dict(countries))),
                balance=random.randint(10_000, 1_000_000),
                car_characteristics={
                    characteristic1.name: characteristic1.value,
                    characteristic2.name: characteristic2.value
                },
                discount=random.randint(0, 10),
            )

    class CarCharacteristics(Enum):
        body_type = random.choice(list(CarTypeEnum)).value
        fuel = random.choice(list(CarFuelEnum)).value
        brand = random.choice(list(CarBrandEnum)).value

    def _generate_random_string(self, length=10):
        letters = string.ascii_lowercase + string.digits
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def _generate_random_date(self, start_date, end_date):
        random_days = random.randint(0, (end_date - start_date).days)
        random_date = start_date + timedelta(days=random_days)
        return random_date
