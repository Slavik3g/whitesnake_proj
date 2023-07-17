from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import SuppliersViewSet, SupplierCarViewSet, SuppliersDiscountView

supplier_router = SimpleRouter()
supplier_router.register('supplier', SuppliersViewSet, basename='supplier')

suppliers_car_router = SimpleRouter()
suppliers_car_router.register('cars', SupplierCarViewSet,basename='supplier_car')

urlpatterns = [
    path('api/', include(supplier_router.urls)),
    path('api/supplier/', include(suppliers_car_router.urls)),
    path('api/supplier/discount/', SuppliersDiscountView.as_view()),
]
