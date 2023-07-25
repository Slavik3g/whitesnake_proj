from rest_framework.routers import SimpleRouter
from .views import CarViewSet, BaseUserViewSet
from django.urls import path, include

car_router = SimpleRouter()
car_router.register('car', CarViewSet)

user_router = SimpleRouter()
user_router.register('user', BaseUserViewSet)

urlpatterns = [
    path('api/', include(car_router.urls)),
    path('api/', include(user_router.urls))
]


