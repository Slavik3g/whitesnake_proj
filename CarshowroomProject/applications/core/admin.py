from django.contrib import admin
from applications.core.models import CarModel, BaseUser

admin.site.register((CarModel, BaseUser))
