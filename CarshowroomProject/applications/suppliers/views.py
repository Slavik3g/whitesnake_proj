from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from applications.core.mixins import SafeDeleteModelMixin
from .filters import SupplierFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import SupplierModel, SupplierCarModel, SupplierDiscount
from .serializers import SupplierSerializer, SupplierCarSerializer, SupplierDiscountSerializer
from .services import SupplierService


class SuppliersViewSet(GenericViewSet,
                       ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       SafeDeleteModelMixin, ):
    serializer_class = SupplierSerializer
    queryset = SupplierModel.objects.all()
    filter_backends = (DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter,
                       )
    filterset_class = SupplierFilter
    ordering_fields = ('id', 'name', 'created_year',)
    search_fields = ('id', 'name')
    service = SupplierService()
    # permission_classes = (permissions.AllowAny,)
    @action(methods=['GET'], detail=True)
    def get_statistic(self, request, pk):
        supplier = self.service.get_supplier(pk)
        statistics_data = self.service.get_statistics_data(supplier)
        return Response(data=statistics_data, status=status.HTTP_200_OK)


class SupplierCarViewSet(GenericViewSet,
                         ListModelMixin,
                         CreateModelMixin, ):
    queryset = SupplierCarModel.objects.all()
    serializer_class = SupplierCarSerializer
    permission_classes = (permissions.AllowAny,)


class SupplierDiscountView(ListCreateAPIView, ):
    queryset = SupplierDiscount.objects.all()
    serializer_class = SupplierDiscountSerializer
    permission_classes = (permissions.AllowAny,)

