from ..models import Apartment, COMMUNAL_SERVICE_TARIFF, BuildingServiceLog
from .tariff import TariffEntity


class BuildingServiceLogEntity:
    @staticmethod
    def get_n_set_price(apartment_id, year, month):
        """Get price for the building service for an apartment and set it.
        It the price is already found, set nothing then."""
        bsl = BuildingServiceLog.objects.filter(apartment_id=apartment_id, month=month, year=year).first()
        if bsl is not None: return bsl.price
        apartment = Apartment.objects.get(id=apartment_id)
        communal_service_unit_price = TariffEntity.get_price_by(COMMUNAL_SERVICE_TARIFF)
        price = apartment.size_m2 * communal_service_unit_price
        bsl = BuildingServiceLog(apartment_id=apartment_id, month=month, year=year, price=price)
        bsl.save()
        return price
        