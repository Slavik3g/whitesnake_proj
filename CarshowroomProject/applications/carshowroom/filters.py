from .models import CarShowroomModel
from django_filters import rest_framework as filters
from django_countries import countries


class CarShowroomFilter(filters.FilterSet):
    country = filters.ChoiceFilter(choices=countries)
    balance_gte = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance_lte = filters.NumberFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = CarShowroomModel
        fields = ['country', 'balance', ]
