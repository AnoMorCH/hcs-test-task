from django.db import models


class Building(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.SmallIntegerField()
    address = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["number", "address"], name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f"{self.address}, {self.number}"

        
class Apartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.SmallIntegerField()
    building_id = models.ForeignKey(Building, to_field="id", on_delete=models.CASCADE)
    size_m2 = models.SmallIntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["number", "building_id"], name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f"{self.building_id}, {self.number}"

        
class WaterMeter(models.Model):
    id = models.BigAutoField(primary_key=True)
    apartment_id = models.ForeignKey(Apartment, to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return f'Meter #{self.id} at address "{self.apartment_id}"'

    
class Tariff(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=32)
    unit_price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type"], name="%(app_label)s_%(class)s_unique")
        ]
