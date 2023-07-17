from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from .mixins import SafeDeleteModelMixin
from .serializers import CarSerializer, BaseUserSerializer
from .models import CarModel, BaseUser
from rest_framework import mixins


class CarViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.CreateModelMixin,
                 SafeDeleteModelMixin,
                 GenericViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
