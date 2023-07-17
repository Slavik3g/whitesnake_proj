from rest_framework import serializers

from .models import CarShowroomModel, CarShowroomDiscount


class CarShowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShowroomModel
        fields = '__all__'
