from django.db.models import Sum

from .models import CustomerModel, CustomerPurchaseHistoryModel


class CustomerService:
    def get_customer(self, customer_id):
        return CustomerModel.objects.get(user=customer_id)

    def get_customer_purchase_hist(self, customer, car=None):
        filters = {
            'customer': customer
        }
        if car:
            filters['car'] = car

        return CustomerPurchaseHistoryModel.objects.filter(**filters)

    def get_statistics_data(self, customer):
        statistics = {"total spend money": self.get_total_spend_money(customer),
                      'customer cars': self.get_customer_cars(customer)}
        return statistics

    def get_customer_cars(self, customer):
        unique_purchase_history_set = self.get_customer_purchase_hist(customer=customer).distinct('car')
        customer_cars = {}

        for unique_purchase_history in unique_purchase_history_set:
            car = unique_purchase_history.car
            customer_cars[
                car.brand + " " + car.model
                ] = self.get_customer_purchase_hist(customer=customer, car=car).count()
            return customer_cars

    def get_total_spend_money(self, customer):
        price = self.get_customer_purchase_hist(customer=customer).aggregate(Sum('price'))['price__sum']
        return price if price else 0
