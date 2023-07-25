from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer,OfferSerializer
from .models import CustomerModel, OfferModel
from applications.core.mixins import SafeDeleteModelMixin
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from .services import CustomerService


class CustomerViewSet(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin,
                      CreateModelMixin,
                      SafeDeleteModelMixin):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'user'
    service = CustomerService()
    permission_classes = (permissions.AllowAny,)


class OfferViewSet(GenericViewSet,
                   CreateModelMixin):
    # permission_classes = (IsAuthenticated, EmailConfirmPermission)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OfferSerializer
    queryset = OfferModel.objects.all()

    def perform_create(self, serializer):
        customer_instance = get_object_or_404(CustomerModel, user=self.request.user)

        serializer.save(customer=customer_instance, is_active=True)



