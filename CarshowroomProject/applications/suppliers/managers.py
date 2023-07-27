from django.utils import timezone

from django.db import models
from django.db.models import Q


class SupplierDiscountQuerySet(models.query.QuerySet):
    def get_active_discounts(self, car, supplier):
        return self.filter(Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(supplier=supplier))


