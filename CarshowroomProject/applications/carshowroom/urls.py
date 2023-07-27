from rest_framework.routers import SimpleRouter
from .views import CarShowroomViewSet, CarshowroomDiscountView
from django.urls import include, path

carshowroom_router = SimpleRouter()
carshowroom_router.register('carshowrooms', CarShowroomViewSet)
urlpatterns = [
    path('api/', include(carshowroom_router.urls)),
    path('api/carshowroom/discount/', CarshowroomDiscountView.as_view()),

]
