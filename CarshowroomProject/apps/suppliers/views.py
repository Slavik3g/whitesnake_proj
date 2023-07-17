from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.core.mixins import SafeDeleteModelMixin

from .models import SupplierModel
from .serializers import SupplierSerializer, SupplierCarSerializer, SupplierDiscountSerializer


class SuppliersViewSet(GenericViewSet,
                       ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       SafeDeleteModelMixin,):
    serializer_class = SupplierSerializer
    queryset = SupplierModel.objects.all()
    permission_classes = (permissions.AllowAny,)


class SupplierCarViewSet(GenericViewSet,
                         CreateModelMixin,):
    serializer_class = SupplierCarSerializer
    permission_classes = (permissions.AllowAny,)


class SuppliersDiscountView(CreateAPIView):
    serializer_class = SupplierDiscountSerializer
    permission_classes = (permissions.AllowAny,)
