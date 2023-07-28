from django.db.models import Sum

from applications.carshowroom.models import CarShowroomModel, CarShowroomSupplierPurchaseHistory
from applications.customers.models import CustomerPurchaseHistoryModel


class CarshowroomService:
    def create_carshowroom(self, carshowroom_data):
        carshowroom, created = CarShowroomModel.objects.get_or_create(**carshowroom_data)
        return carshowroom

    def get_carshowroom(self, id):
        return CarShowroomModel.objects.get(id=id)

    def get_statistics_data(self):
        statistics = {
            'total_amount_of_purchases': self.total_count_of_purchases(),
            'total_spend_money': self.get_total_spend_money(),
            'total_income_money': self.total_income_money(),

        }

    #
    # def total_count_of_purchases(self):
    #     CustomerPurchaseHistoryModel.objects.

    def total_income_money(self):
        total_income = CustomerPurchaseHistoryModel.objects.all().aggregate(total_price=Sum('price'))['total_price']
        return total_income if total_income else 0

    def get_total_spend_money(self):
        total_spend = CarShowroomSupplierPurchaseHistory.objects.all().aggregate(total_spend=Sum('total_price'))['total_spend']
        return total_spend if total_spend else 0
