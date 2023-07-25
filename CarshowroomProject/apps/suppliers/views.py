from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.core.mixins import SafeDeleteModelMixin

from .models import SupplierModel, SupplierCarModel, SupplierDiscount
from .serializers import SupplierSerializer, SupplierCarSerializer, SupplierDiscountSerializer


class SuppliersViewSet(GenericViewSet,
                       ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       SafeDeleteModelMixin, ):
    serializer_class = SupplierSerializer
    queryset = SupplierModel.objects.all()
    permission_classes = (permissions.AllowAny, )



class SupplierCarViewSet(GenericViewSet,
                         ListModelMixin,
                         CreateModelMixin, ):
    queryset = SupplierCarModel.objects.all()
    serializer_class = SupplierCarSerializer
    permission_classes = (permissions.AllowAny, )


class SupplierDiscountView(ListCreateAPIView, ):
    queryset = SupplierDiscount.objects.all()
    serializer_class = SupplierDiscountSerializer
    permission_classes = (permissions.AllowAny, )
