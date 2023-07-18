from django.contrib import admin
from apps.core.models import CarModel, BaseUser

admin.site.register((CarModel, BaseUser))
