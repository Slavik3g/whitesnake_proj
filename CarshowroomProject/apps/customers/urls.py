from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import CustomerViewSet
from django.urls import path, include

router = SimpleRouter()
router.register('customer', CustomerViewSet)

urlpatterns = []
urlpatterns += router.urls