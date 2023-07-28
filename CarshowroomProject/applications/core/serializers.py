from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CarModel, BaseUser


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'fuel', 'body_type', 'model',)
        read_only_fields = ('id',)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password',)
        # read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RestorePasswordEmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not BaseUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email does not exist in our records.")
        return value


