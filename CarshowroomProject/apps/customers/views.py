from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer
from .models import CustomerModel
from apps.core.mixins import SafeDeleteModelMixin
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin


class CustomerViewSet(GenericViewSet,
                      CreateModelMixin,
                      ListModelMixin,
                      RetrieveModelMixin,
                      SafeDeleteModelMixin):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.AllowAny, )

