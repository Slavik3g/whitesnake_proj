
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from .yasg import urlpatterns as swagger_urls
from apps.core.urls import urlpatterns as core_urls
from apps.suppliers.urls import urlpatterns as suppliers_urls
from apps.customers.urls import urlpatterns as customer_urls
from apps.carshowroom.urls import urlpatterns as carshowroom_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += core_urls + suppliers_urls + customer_urls + carshowroom_urls
urlpatterns += swagger_urls
