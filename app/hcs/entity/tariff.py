from ..models import WATER_TARIFF, COMMUNAL_SERVICE_TARIFF, Tariff

class TariffEntity:
    @staticmethod
    def get_price_by(type):
        if type == WATER_TARIFF:
            return Tariff.objects.get(type=WATER_TARIFF).unit_price
        elif type == COMMUNAL_SERVICE_TARIFF:
            return Tariff.objects.get(type=COMMUNAL_SERVICE_TARIFF).unit_price
    