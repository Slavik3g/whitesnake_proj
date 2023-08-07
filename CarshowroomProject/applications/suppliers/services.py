from django.db.models import Sum

from applications.carshowroom.models import CarShowroomSupplierPurchaseHistory
from applications.suppliers.models import SupplierModel, SupplierCarModel


class SupplierService:
    def create_supplier(self, supplier_data):
        supplier, created = SupplierModel.objects.get_or_create(**supplier_data)
        return supplier

    def get_supplier(self, id):
        return SupplierModel.objects.get(id=id)

    def get_statistics_data(self, supplier):
        statistics = {
            "supplier cars": self.get_supplier_cars(supplier),
            "income money": self.get_supplier_income_money(supplier)
        }

        clients_stats = {}
        clients_purchases_set = self.clients_purchases_set(supplier=supplier)

        for clients_purchases in clients_purchases_set:
            carshowroom = clients_purchases.carshowroom
            clients_stats[str(carshowroom.id) + " " + carshowroom.name] = self.get_number_of_sold_cars(
                supplier=supplier,
                carshowroom=carshowroom
            )
        statistics['number of clients bought cars'] = clients_stats
        return statistics

    def get_supplier_cars(self, supplier):
        cars = []
        supplier_cars = SupplierCarModel.objects.filter(supplier=supplier)
        for supplier_car in supplier_cars:
            cars.append((supplier_car.car.brand, supplier_car.car.model))
        return cars

    def get_supplier_income_money(self, supplier):
        total_income = CarShowroomSupplierPurchaseHistory.objects.filter(supplier=supplier) \
            .aggregate(Sum('total_price'))
        return total_income if total_income else 0

    def clients_purchases_set(self, supplier):
        return CarShowroomSupplierPurchaseHistory.objects.filter(supplier=supplier)

    def get_number_of_sold_cars(self, supplier, carshowroom):
        filters = {
            'supplier': supplier,
            'carshowroom': carshowroom
        }

        data = CarShowroomSupplierPurchaseHistory.objects.filter(**filters).aggregate(Sum('cars_count'))[
            'cars_count__sum']
        return data if data else 0
