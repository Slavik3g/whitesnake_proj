from django.contrib import admin
from apps.customers.models import CustomerModel, CustomerPurchaseHistoryModel

admin.site.register((CustomerModel, CustomerPurchaseHistoryModel))
