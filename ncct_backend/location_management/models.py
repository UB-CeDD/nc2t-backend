from django.db import models

class Location(models.Model):
    continent = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    region_state = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.city_town}, {self.country}"

