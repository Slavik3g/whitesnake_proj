from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer
from .models import CustomerModel
from applications.core.mixins import SafeDeleteModelMixin
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from .services import CustomerService


class CustomerViewSet(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin,
                      SafeDeleteModelMixin):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'user'
    service = CustomerService()
    permission_classes = (permissions.AllowAny,)
