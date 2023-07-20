from rest_framework import serializers

from .models import SupplierModel, SupplierCarModel, SupplierDiscount
from apps.core.models import CarModel


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModel
        fields = ('id', 'name', 'created_year', 'cars_list', 'discount', 'count_of_customers', 'balance')
        read_only_fields = ('id',)


class SupplierCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCarModel
        exclude = ('is_active',)


class SupplierDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDiscount
        exclude = ('is_active',)
