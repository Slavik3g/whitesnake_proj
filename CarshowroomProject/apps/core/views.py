from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from .mixins import SafeDeleteModelMixin
from .serializers import CarSerializer, BaseUserSerializer
from .models import CarModel, BaseUser
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin


class CarViewSet(GenericViewSet,
                 ListModelMixin,
                 RetrieveModelMixin,
                 UpdateModelMixin,
                 CreateModelMixin,
                 SafeDeleteModelMixin,):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer


class BaseUserViewSet(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      CreateModelMixin,
                      SafeDeleteModelMixin,):
    permission_classes = (permissions.AllowAny,)
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
