from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator


UNIQUE_CONSTRAINT_NAME_PATTERN = "%(app_label)s_%(class)s_unique"

WATER_TARIFF = "WATER"
COMMUNAL_SERVICE_TARIFF = "COMMUNAL SERVICE"


class Building(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.SmallIntegerField()
    address = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["number", "address"], name=UNIQUE_CONSTRAINT_NAME_PATTERN)
        ]

    def __str__(self):
        return f"Address: {self.address}, {self.number}"

        
class Apartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.SmallIntegerField()
    building = models.ForeignKey(Building, to_field="id", on_delete=models.CASCADE)
    size_m2 = models.SmallIntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["number", "building"], name=UNIQUE_CONSTRAINT_NAME_PATTERN)
        ]

    def __str__(self):
        return f"{self.building}. Number: {self.number}"

        
class WaterMeter(models.Model):
    id = models.BigAutoField(primary_key=True)
    apartment = models.ForeignKey(Apartment, to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return f'Meter #{self.id} at address "{self.apartment}"'

    
class Tariff(models.Model):
    TYPE_CHOICES = [
        (WATER_TARIFF, "Water"),
        (COMMUNAL_SERVICE_TARIFF, "Communal Service")
    ]

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    unit_price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type"], name=UNIQUE_CONSTRAINT_NAME_PATTERN),
            models.CheckConstraint(
                check=Q(type__in=[WATER_TARIFF, COMMUNAL_SERVICE_TARIFF]),
                name="status_valid"
            )
        ]

    def __str__(self):
        return str(self.type)

        
class WaterMeterLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    water_meter = models.ForeignKey(WaterMeter, to_field="id", on_delete=models.CASCADE)
    month = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.SmallIntegerField()
    consumed = models.SmallIntegerField()
    price = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["water_meter_id", "month", "year"], name=UNIQUE_CONSTRAINT_NAME_PATTERN)
        ]

    def __str__(self):
        return f"Water meter #{self.water_meter} on {self.year} year and {self.month} month"


class BuildingServiceLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    apartment = models.ForeignKey(Apartment, to_field="id", on_delete=models.CASCADE)
    month = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.SmallIntegerField()
    price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["apartment_id", "month", "year"], name=UNIQUE_CONSTRAINT_NAME_PATTERN)
        ]

    def __str__(self):
        return f"Apartment id {self.apartment} on {self.year} year and {self.month} month"
