from ..models import Apartment
from .water_meter import WaterMeterEntity


class ApartmentEntity:
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