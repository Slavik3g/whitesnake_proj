from rest_framework.routers import DefaultRouter
from .views import CarViewSet, BaseUserViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('car', CarViewSet)
router.register('user', BaseUserViewSet)

urlpatterns = []
urlpatterns += router.urls


