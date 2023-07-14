from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

from .serializers import CarSerializer, BaseUserSerializer
from .models import CarModel, BaseUser
from rest_framework import mixins


class CarViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
