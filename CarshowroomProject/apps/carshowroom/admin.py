from django.contrib import admin

from apps.carshowroom.models import CarShowroomModel, CarShowroomCar, CarShowroomDiscount, CarShowroomSupplierPurchaseHistory

admin.site.register((CarShowroomModel, CarShowroomCar, CarShowroomDiscount, CarShowroomSupplierPurchaseHistory))
