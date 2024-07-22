from ..models import Apartment, WaterMeter


class WaterMeterEntity:
    @staticmethod
    def create(apartment_id):
        water_meter = WaterMeter(apartment=Apartment(id=apartment_id))
        water_meter.save()

    @staticmethod
    def get_by(apartment_id):
        return WaterMeter.objects.filter(apartment_id=apartment_id)

    @staticmethod
    def get_info_by(apartment_id):
        info = []
        water_meters = WaterMeter.objects.filter(apartment_id=apartment_id).values()
        for water_meter in water_meters:
            del water_meter["apartment_id"]
            info.append(water_meter)
        return info
