from rest_framework import serializers

from .models import CarShowroomModel, CarShowroomDiscount


class CarShowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShowroomModel
        fields = ('id', 'name', 'country', 'car_characteristics', 'balance', 'discount',)
        read_only_fields = ('id',)


class CarshowroomDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShowroomDiscount
        exclude = ('is_active',)
