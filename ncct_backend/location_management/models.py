import uuid
import secrets
from django.db import models

# Function to generate a random string
def generate_unique_id():
    return secrets.token_urlsafe(16)

class Location(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    continent = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    region_state = models.CharField(max_length=255, blank=True)
    city_town = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255, blank=True)
    place = models.CharField(max_length=255, blank=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    voucher_specimen_number = models.CharField(max_length=255, blank=True, null=True, help_text="Optional voucher specimen number")

    def __str__(self):
        return f"{self.name}, {self.city_town}, {self.country}"

class Site(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name