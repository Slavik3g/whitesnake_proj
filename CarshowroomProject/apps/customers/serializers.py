from rest_framework import serializers

from .models import CustomerModel


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ('user', 'balance')
