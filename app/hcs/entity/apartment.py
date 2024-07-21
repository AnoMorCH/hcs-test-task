from ..models import Apartment, Building
from .water_meter import WaterMeterEntity


class ApartmentEntity:
    @staticmethod
    def create(number, building_id, size_m2):
        if not all([number, building_id, size_m2]):
            raise AttributeError("There is no number, building id or size m2.")
        apartment = Apartment(
            number=number, 
            building=Building.objects.get(id=building_id), 
            size_m2=size_m2
        )
        apartment.save()

    @staticmethod
    def get_info_by(building_id):
        info = []
        apartments = Apartment.objects.filter(building_id=building_id).values()
        for apartment in apartments:
            apartment_info = apartment
            apartment_info["water_meters"] = WaterMeterEntity.get_info_by(apartment["id"])
            del apartment_info["building_id"]
            info.append(apartment_info)
        return info