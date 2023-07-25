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
    permission_classes = (permissions.AllowAny, )



class BaseUserViewSet(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      CreateModelMixin,
                      SafeDeleteModelMixin,):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (permissions.AllowAny, )

