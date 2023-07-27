from applications.suppliers.models import SupplierModel


class SupplierService():
    def create_supplier(self, supplier_data):
        supplier, created = SupplierModel.objects.get_or_create(**supplier_data)
        return supplier

    def get_supplier(self, id):
        return SupplierModel.objects.get(id=id)
