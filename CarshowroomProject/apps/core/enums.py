from enum import Enum


class CarTypeEnum(Enum):
    MICRO = 'micro'
    SEDAN = 'sedan'
    HATCHBACK = 'hatchback'
    UNIVERSAL = 'universal'
    COUPE = 'coupe'
    CABRIOLET = 'cabriolet'
    ROADSTER = 'roadster'
    TARGA = 'targa'
    LIMOUSINE = 'limousine'
    MUSCLE_CAR = 'muscle_car'
    SPORT_CAR = 'sport car'
    SUPER_CAR = 'super car'
    CROSSOVER = 'crossover'
    PICKUP = 'pickup'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class CarFuelEnum(Enum):
    PETROL = 'petrol'
    DIESEL = 'diesel'
    ELECTRIC = 'electric'
    BIOFUEL = 'biofuel'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class CarBrandEnum(Enum):
    BMW = 'bmw'
    SUBARU = 'subaru'
    LEXUS = 'lexus'
    HONDA = 'honda'
    TOYOTA = 'toyota'
    MAZDA = 'mazda'
    AUDI = 'audi'
    KIA = 'kia'
    HYUNDAI = 'hyundai'
    PORSCHE = 'porsche'
    TESLA = 'tesla'
    INFINITI = 'infiniti'
    VOLKSWAGEN = 'volkswagen'
    VOLVO = 'volvo'
    NISSAN = 'nissan'
    FORD = 'ford'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]