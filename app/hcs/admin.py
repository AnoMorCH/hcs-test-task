from django.contrib import admin
from .models import Building, Apartment, WaterMeter, Tariff, BuildingServiceLog, WaterMeterLog


admin.site.register([
    Building,
    Apartment,
    WaterMeter,
    Tariff,
    BuildingServiceLog,
    WaterMeterLog,
])

