from django.contrib import admin
from applications.customers.models import CustomerModel, CustomerPurchaseHistoryModel

admin.site.register((CustomerModel, CustomerPurchaseHistoryModel))
