from django.shortcuts import render
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import CarShowroomSerializer
from .models import CarShowroomModel
from apps.core.mixins import SafeDeleteModelMixin
from .filters import CarShowroomFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class CarShowroomViewSet(GenericViewSet,
                         CreateModelMixin,
                         ListModelMixin,
                         RetrieveModelMixin,
                         DestroyModelMixin):
    serializer_class = CarShowroomSerializer
    queryset = CarShowroomModel.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter,
                       )
    filterset_class = CarShowroomFilter
    ordering_fields = ('id', 'name', 'country', 'balance', 'discount')
    search_fields = ('id', 'name', 'country', 'discount')
