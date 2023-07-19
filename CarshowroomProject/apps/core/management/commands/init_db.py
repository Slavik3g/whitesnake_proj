import random
import string
from enum import Enum

from django.core.management.base import BaseCommand
from apps.core.models import CarModel
from apps.core.enums import CarBrandEnum, CarFuelEnum, CarTypeEnum
from apps.carshowroom.models import CarShowroomModel
from django_countries import countries


class CarCharacteristics(Enum):
    body_type = random.choice(list(CarTypeEnum)).value
    fuel = random.choice(list(CarFuelEnum)).value
    brand = random.choice(list(CarBrandEnum)).value


def generate_random_string(length=10):
    letters = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        self._create_cars()
        self._create_showrooms()

    def _create_cars(self):
        for _ in range(10):
            CarModel.objects.get_or_create(
                brand=random.choice(list(CarBrandEnum)).value,
                fuel=random.choice(list(CarFuelEnum)).value,
                body_type=random.choice(list(CarTypeEnum)).value,
                model=generate_random_string(5),
            )

    def _create_showrooms(self):
        for _ in range(20):
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
