from rest_framework import viewsets
from .serializers import CustomerSerializer
from .models import CustomerModel
from rest_framework import mixins


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer
