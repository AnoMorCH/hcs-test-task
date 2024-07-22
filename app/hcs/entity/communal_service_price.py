from ..models import Building
from .apartment import ApartmentEntity
from .water_meter import WaterMeterEntity
from .water_meter_log import WaterMeterLogEntity
from .building_service_log import BuildingServiceLogEntity


class CommunalServicePrice:
    def __init__(self, building_id, year, month):
        self.building = Building.objects.get(id=building_id)
        self.year = year
        self.month = month

    def count(self):
        apartments = ApartmentEntity.get_by(self.building.id)
        total_price = 0
        for apartment in apartments:
            for water_meter in WaterMeterEntity.get_by(apartment.id):
                total_price += WaterMeterLogEntity.get_n_set_price(water_meter.id, self.month, self.year)
            total_price += BuildingServiceLogEntity.get_n_set_price(apartment.id, self.year, self.month)
        return total_price
    