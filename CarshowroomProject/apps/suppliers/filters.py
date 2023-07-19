from django_filters import rest_framework as filters
from .models import SupplierModel


class SupplierFilter(filters.FilterSet):
    created_year_gte = filters.DateFilter(field_name='created_year', lookup_expr='gte')
    created_year_lte = filters.DateFilter(field_name='created_year', lookup_expr='lte')
    balance_gte = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance_lte = filters.NumberFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = SupplierModel
        fields = ['created_year', 'balance', ]
