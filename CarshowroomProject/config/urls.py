
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .settings import DEBUG
from .yasg import urlpatterns as swagger_urls
from apps.core.urls import urlpatterns as core_urls
from apps.suppliers.urls import urlpatterns as suppliers_urls
from apps.customers.urls import urlpatterns as customer_urls
from apps.carshowroom.urls import urlpatterns as carshowroom_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += core_urls + suppliers_urls + customer_urls + carshowroom_urls
urlpatterns += swagger_urls

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
