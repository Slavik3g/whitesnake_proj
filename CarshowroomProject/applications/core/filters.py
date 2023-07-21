from django_filters import rest_framework as filters
from .models import CarModel
from .enums import CarBrandEnum, CarTypeEnum, CarFuelEnum


class CarFilter(filters.FilterSet):
    brand = filters.ChoiceFilter(choices=CarBrandEnum.choices())
    fuel = filters.ChoiceFilter(choices=CarFuelEnum.choices())
    body_type = filters.ChoiceFilter(choices=CarTypeEnum.choices())

    class Meta:
        model = CarModel
        fields = ['brand', 'body_type', 'fuel']
