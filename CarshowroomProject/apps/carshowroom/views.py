from django.shortcuts import render
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import CarShowroomSerializer
from .models import CarShowroomModel
from apps.core.mixins import SafeDeleteModelMixin


# Create your views here.

class CarShowroomViewSet(GenericViewSet,
                         CreateModelMixin,
                         ListModelMixin,
                         RetrieveModelMixin,
                         SafeDeleteModelMixin):
    serializer_class = CarShowroomSerializer
    queryset = CarShowroomModel.objects.all()
    permission_classes = (permissions.AllowAny, )


