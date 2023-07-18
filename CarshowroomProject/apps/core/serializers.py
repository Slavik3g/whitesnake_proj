from rest_framework import serializers

from .models import CarModel, BaseUser


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'fuel', 'type', 'model',)
        read_only_fields = ('id',)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
