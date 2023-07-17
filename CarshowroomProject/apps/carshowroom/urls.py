from rest_framework.routers import SimpleRouter
from .views import CarShowroomViewSet
from django.urls import include, path

carshowroom_router = SimpleRouter()
carshowroom_router.register('carshowroom', CarShowroomViewSet)
urlpatterns = [
    path('api/', include(carshowroom_router.urls))
]
