from rest_framework import serializers

from .models import SupplierModel


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModel
        fields = '__all__'
