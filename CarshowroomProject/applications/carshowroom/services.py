from applications.carshowroom.models import CarShowroomModel


class CarshowroomService:
    def create_carshowroom(self, carshowroom_data):
        carshowroom, created = CarShowroomModel.objects.get_or_create(**carshowroom_data)
        return carshowroom

    def get_carshowroom(self, id):
        return CarShowroomModel.objects.get(id=id)
