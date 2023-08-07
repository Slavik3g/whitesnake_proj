from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import CarShowroomSerializer, CarshowroomDiscountSerializer
from .models import CarShowroomModel, CarShowroomDiscount
from applications.core.mixins import SafeDeleteModelMixin
from .filters import CarShowroomFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .services import CarshowroomService


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
    service = CarshowroomService()

    @action(methods=['GET'], detail=True)
    def get_statistic(self, request, pk):
        carshowroom = self.service.get_carshowroom(pk)
        statistic_data = self.service.get_statistics_data(carshowroom)
        return Response(data=statistic_data, status=status.HTTP_200_OK)


class CarshowroomDiscountView(ListCreateAPIView, ):
    queryset = CarShowroomDiscount.objects.all()
    serializer_class = CarshowroomDiscountSerializer
    permission_classes = (permissions.AllowAny,)
