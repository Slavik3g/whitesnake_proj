from django.contrib import admin
from apps.suppliers.models import SupplierModel, SupplierCar, SupplierDiscount

admin.site.register((SupplierModel, SupplierCar, SupplierDiscount))
