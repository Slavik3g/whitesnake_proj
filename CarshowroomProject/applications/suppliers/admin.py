from django.contrib import admin
from applications.suppliers.models import SupplierModel, SupplierCarModel, SupplierDiscount

admin.site.register((SupplierModel, SupplierCarModel, SupplierDiscount))
