from rest_framework.routers import SimpleRouter
from .views import CarViewSet, BaseUserViewSet, RestorePasswordEmailSendView, RestorePasswordConfirmView
from django.urls import path, include

car_router = SimpleRouter()
car_router.register('cars', CarViewSet)

user_router = SimpleRouter()
user_router.register('user', BaseUserViewSet, basename='user')

urlpatterns = [
    path('api/', include(car_router.urls)),
    path('api/', include(user_router.urls)),
    path('api/reset_password/', RestorePasswordEmailSendView.as_view()),
    path('api/reset_password/confirm/<uidb64>/<token>/', RestorePasswordConfirmView.as_view()),

]


