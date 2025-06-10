from django.db import models
from ncct_backend.compound_management.models import Compound
from ncct_backend.location_management.models import Location
from ncct_backend.reference_management.models import Reference

# Species model
class Species(models.Model):
    unique_id = models.AutoField(primary_key=True)
    compound_code = models.IntegerField()
    ref = models.ForeignKey(Reference, on_delete=models.CASCADE)
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

