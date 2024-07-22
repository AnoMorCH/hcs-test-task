from ..models import WaterMeter, WaterMeterLog, WATER_TARIFF
from .water_consumption import WaterConsumption
from .tariff import TariffEntity


class WaterMeterLogEntity:
    @staticmethod
    def create(water_meter_id, month, year, consumed):
        water_meter_log = WaterMeterLog(
            water_meter=WaterMeter.objects.get(id=water_meter_id),
            month=month,
            year=year,
            consumed=consumed
        )
        water_meter_log.save()

    @staticmethod
    def get_n_set_price(water_meter_id, month, year):
        """Get and set price for a current month and year of a water meter.
        If the price is already found, return it instead and set nothing."""
        water_meter_log = WaterMeterLog.objects.filter(
            water_meter_id=water_meter_id,
            month=month,
            year=year
        ).first()
        is_price_already_found = water_meter_log.price is not None
        if is_price_already_found: return water_meter_log.price
        wc = WaterConsumption(water_meter_id, year, month)
        wc_value = wc.count()
        water_unit_price = TariffEntity.get_price_by(WATER_TARIFF)
        price = water_unit_price * wc_value
        water_meter_log.price = price
        water_meter_log.save()
        return price
