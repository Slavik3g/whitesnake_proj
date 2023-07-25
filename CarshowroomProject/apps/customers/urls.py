from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import CustomerViewSet
from django.urls import path, include

customer_router = SimpleRouter()
customer_router.register('customer', CustomerViewSet)

urlpatterns = [
    path('api/', include(customer_router.urls)),
]
