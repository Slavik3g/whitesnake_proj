from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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

    def validate_max_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Значение поля max_price должно быть неотрицательным.")
        return value

    def validate(self, data):
        max_price = data.get('max_price')
        customer = get_object_or_404(CustomerModel, user=self.context['request'].user)
        if max_price is not None and max_price > customer.balance:
            raise serializers.ValidationError("Значение поля max_price не должно превышать баланса пользователя.")
        return data

