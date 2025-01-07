from django.db import models

class FuelPrice(models.Model):
    opis_truckstop_id = models.CharField(max_length=255)
    truckstop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    rack_id = models.CharField(max_length=255)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state} - {self.retail_price}"
