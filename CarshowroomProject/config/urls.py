
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from .yasg import urlpatterns as swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.customers.urls')),
    path('api/', include('apps.core.urls')),
]

urlpatterns += swagger_urls