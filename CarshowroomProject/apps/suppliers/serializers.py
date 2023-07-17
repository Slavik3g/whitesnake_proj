from rest_framework import serializers

from .models import SupplierModel, SupplierCar, SupplierDiscount
from apps.core.models import CarModel


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModel
        fields = ('name', 'created_year', 'cars_list', 'discount', 'count_of_customers', 'balance')
        read_only_fields = ('id',)


class SupplierCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCar
        fields = '__all__'


class SupplierDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDiscount
        fields = '__all__'
