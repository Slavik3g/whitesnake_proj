from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from .mixins import SafeDeleteModelMixin
from .serializers import CarSerializer, BaseUserSerializer
from .models import CarModel, BaseUser
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import CarFilter


class CarViewSet(GenericViewSet,
                 ListModelMixin,
                 RetrieveModelMixin,
                 UpdateModelMixin,
                 CreateModelMixin,
                 SafeDeleteModelMixin, ):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter,
                       )
    filterset_class = CarFilter
    ordering_fields = ('id', 'brand', 'fuel', 'bodys_type', 'model',)
    search_fields = ('id', 'brand', 'fuel', 'body_type', 'model',)


class BaseUserViewSet(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      CreateModelMixin,
                      SafeDeleteModelMixin, ):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (permissions.AllowAny,)
