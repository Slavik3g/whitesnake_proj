from rest_framework import serializers

from .models import CustomerModel, OfferModel


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ('user', 'balance')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferModel
        fields = '__all__'
        read_only_fields = ('customer',)
