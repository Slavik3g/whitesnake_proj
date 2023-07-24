from django.shortcuts import render
from requests import Response
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import CarShowroomSerializer, CarshowroomDiscountSerializer
from .models import CarShowroomModel, CarShowroomDiscount
from applications.core.mixins import SafeDeleteModelMixin
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


class CarshowroomDiscountView(ListCreateAPIView, ):
    queryset = CarShowroomDiscount.objects.all()
    serializer_class = CarshowroomDiscountSerializer
    permission_classes = (permissions.AllowAny,)
