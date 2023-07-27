from django.contrib import admin

from applications.carshowroom.models import CarShowroomModel, CarShowroomCar, CarShowroomDiscount, CarShowroomSupplierPurchaseHistory

admin.site.register((CarShowroomModel, CarShowroomCar, CarShowroomDiscount, CarShowroomSupplierPurchaseHistory))
