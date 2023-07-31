from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer,OfferSerializer
from .models import CustomerModel, OfferModel
from applications.core.mixins import SafeDeleteModelMixin
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from .services import CustomerService
from ..core.permissions import IsEmailConfirmed


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

    @action(methods=['GET'], detail=True)
    def get_statistic(self, request, user):
        customer = self.service.get_customer(user)
        print(customer)
        statistics_data = self.service.get_statistics_data(customer)
        return Response(data=statistics_data, status=status.HTTP_200_OK)

class OfferViewSet(GenericViewSet,
                   CreateModelMixin):
    # permission_classes = (IsAuthenticated, EmailConfirmPermission)
    permission_classes = (IsEmailConfirmed,)
    serializer_class = OfferSerializer
    queryset = OfferModel.objects.all()

    def perform_create(self, serializer):
        customer_instance = get_object_or_404(CustomerModel, user=self.request.user)

        serializer.save(customer=customer_instance, is_active=True)



