from django.db import models
from ncct_backend.compound_management.models import Compound

# Species model
class Species(models.Model):
    unique_id = models.AutoField(primary_key=True)
    compound_code = models.IntegerField()
    ref = models.ForeignKey('Reference', on_delete=models.CASCADE)
    collection_data = models.TextField()

    def __str__(self):
        return f"Species {self.unique_id}"

# Species-Compound many-to-many relationship
class SpeciesCompound(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('species', 'compound'),)  # Ensure that the same combination is unique

    def __str__(self):
        return f"{self.species.unique_id} - {self.compound.subclass}"

# Location model
class Location(models.Model):
    unique_id = models.AutoField(primary_key=True)
    continent = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    region_state = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city_town}, {self.country}"

# Site model
class Site(models.Model):
    unique_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"Site {self.unique_id}"

# Species-Site many-to-many relationship
class SpeciesSite(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('species', 'site'),)

    def __str__(self):
        return f"{self.species.unique_id} - {self.site.unique_id}"

# Herbarium model
class Herbarium(models.Model):
    unique_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"Herbarium {self.unique_id}"

# Species-Herbarium many-to-many relationship
class SpeciesHerbarium(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    herbarium = models.ForeignKey(Herbarium, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('species', 'herbarium'),)

    def __str__(self):
        return f"{self.species.unique_id} - {self.herbarium.unique_id}"

# Reference model
class Reference(models.Model):
    unique_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    thesis_level = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title