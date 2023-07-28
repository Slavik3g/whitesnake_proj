from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import CustomerViewSet, OfferViewSet
from django.urls import path, include

customer_router = SimpleRouter()
customer_router.register('customers', CustomerViewSet)

offer_router = SimpleRouter()
offer_router.register('offer', OfferViewSet)

urlpatterns = [
    path('api/', include(customer_router.urls)),
    path('api/', include(offer_router.urls))
]
