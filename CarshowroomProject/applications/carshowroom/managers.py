from django.utils import timezone

from django.db import models
from django.db.models import Q


class CarShowroomDiscountQuerySet(models.query.QuerySet):
    def get_active_discounts(self, car, carshowroom):
        return self.filter(Q(car_model=car) & Q(discount_end__gt=timezone.now().date()) & Q(carshowroom=carshowroom))


