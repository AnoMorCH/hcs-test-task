from ..models import WaterMeter


class WaterMeterEntity:
    @staticmethod
    def get_info_by(apartment_id):
        info = []
        water_meters = WaterMeter.objects.filter(apartment_id=apartment_id).values()
        for water_meter in water_meters:
            del water_meter["apartment_id"]
            info.append(water_meter)
        return info
