from django.contrib import admin
from apps.suppliers.models import SupplierModel, SupplierCarModel, SupplierDiscount

admin.site.register((SupplierModel, SupplierCarModel, SupplierDiscount))
