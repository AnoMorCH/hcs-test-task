from django.test import TestCase
from .entity.communal_service_price import CommunalServicePrice
from .models import Apartment, Building, WaterMeter, WaterMeterLog, Tariff, WATER_TARIFF, COMMUNAL_SERVICE_TARIFF


class CountCommunalServicePriceTestCase(TestCase):
    BUILDING_ID = 1

    def setUp(self):
        Tariff.objects.create(type=WATER_TARIFF, unit_price=100)
        Tariff.objects.create(type=COMMUNAL_SERVICE_TARIFF, unit_price=200)

        building1 = Building.objects.create(id=self.BUILDING_ID, number=1, address="Hello")
        apartment100 = Apartment.objects.create(number=100, building=building1, size_m2=50)
        water_meter1 = WaterMeter.objects.create(apartment=apartment100)
        water_meter2 = WaterMeter.objects.create(apartment=apartment100)

        WaterMeterLog.objects.create(water_meter=water_meter1, month=1, year=2000, consumed=0)
        WaterMeterLog.objects.create(water_meter=water_meter1, month=2, year=2000, consumed=100)
        WaterMeterLog.objects.create(water_meter=water_meter2, month=1, year=2000, consumed=100)
        WaterMeterLog.objects.create(water_meter=water_meter2, month=2, year=2000, consumed=150)

    def test_count_left(self):
        """Count the price in the middle on the 01-2000 when exists the 
        current month but not the previous one."""
        csp = CommunalServicePrice(self.BUILDING_ID, 2000, 1)
        csp_value = csp.count()
        self.assertEqual(csp_value, 20000)

    def test_count_middle(self):
        """Count the price in the middle on the 02-2000 when exists the 
        previous and the current month."""
        csp = CommunalServicePrice(self.BUILDING_ID, 2000, 2)
        csp_value = csp.count()
        self.assertEqual(csp_value, 25000)

    def test_count_right(self):
        """Count the price in the right on the 03-2000 when exists the
        previous month but no the current month"""
        csp = CommunalServicePrice(self.BUILDING_ID, 2000, 3)
        csp_value = csp.count()
        self.assertEqual(csp_value, 10000)

    def test_count_empty(self):
        """Count the price in the right on the 04-2000 when the previous
        and the current months don't exists."""
        csp = CommunalServicePrice(self.BUILDING_ID, 2000, 4)
        csp_value = csp.count()
        self.assertEqual(csp_value, 10000)
