from rest_framework.routers import SimpleRouter
from django.urls import path, include, re_path
from .views import SuppliersViewSet, SupplierCarViewSet, SupplierDiscountView

supplier_router = SimpleRouter()
supplier_router.register(r'suppliers', SuppliersViewSet)

suppliers_car_router = SimpleRouter()
suppliers_car_router.register(r'cars', SupplierCarViewSet)

urlpatterns = [
    path('api/', include(supplier_router.urls)),
    re_path(r'api/supplier/', include(suppliers_car_router.urls)),
    re_path(r'api/supplier/discount/', SupplierDiscountView.as_view()),
]
