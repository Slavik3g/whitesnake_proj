import random
import string
from datetime import datetime, timedelta
from enum import Enum

from django.core.management.base import BaseCommand
from apps.core.models import CarModel
from apps.core.enums import CarBrandEnum, CarFuelEnum, CarTypeEnum
from apps.carshowroom.models import CarShowroomModel
from django_countries import countries

from apps.suppliers.models import SupplierModel


class CarCharacteristics(Enum):
    body_type = random.choice(list(CarTypeEnum)).value
    fuel = random.choice(list(CarFuelEnum)).value
    brand = random.choice(list(CarBrandEnum)).value


def generate_random_string(length=10):
    letters = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_random_date(start_date, end_date):
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        self._create_cars()
        self._create_showrooms()
        self._generate_suppliers()

    def _generate_suppliers(self):
        for i in range(10):
            random_date = generate_random_date(datetime(1990, 1, 1), datetime.now())
            SupplierModel.objects.get_or_create(
                name=generate_random_string(random.randint(4, 10)),
                created_year=random_date,
                discount=random.randint(0, 10),
                count_of_customers=random.randint(20, 500),
                balance=random.randint(10000, 1000000),
            )

    def _create_cars(self):
        for _ in range(20):
            CarModel.objects.get_or_create(
                brand=random.choice(list(CarBrandEnum)).value,
                fuel=random.choice(list(CarFuelEnum)).value,
                body_type=random.choice(list(CarTypeEnum)).value,
                model=generate_random_string(5),
            )

    def _create_showrooms(self):
        for _ in range(10):
            characteristic1 = random.choice(list(CarCharacteristics))
            characteristic2 = random.choice(list(CarCharacteristics))
            CarShowroomModel.objects.get_or_create(
                name=generate_random_string(random.randint(4, 10)),
                country=random.choice(list(dict(countries))),
                balance=random.randint(10000, 1000000),
                car_characteristics={
                    characteristic1.name: characteristic1.value,
                    characteristic2.name: characteristic2.value
                },
                discount=random.randint(0, 10),
            )
