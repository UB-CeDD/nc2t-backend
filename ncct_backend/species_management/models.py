import secrets
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from ncct_backend.compound_management.models import Compound
from ncct_backend.location_management.models import Location, Site
from ncct_backend.reference_management.models import Reference

# Function to generate a random string
def generate_unique_id():
    return secrets.token_urlsafe(16)

# Habitat model
class Habitat(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Herbarium model
class Herbarium(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Species model
class Species(models.Model):
    PUBLICATION_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    ]
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    recent_name = models.CharField(max_length=255, null=True, blank=True)
    kingdom = models.CharField(max_length=255, null=True, blank=True, default='Plantae')
    trad_uses = models.CharField(max_length=255, null=True, blank=True)
    part_used = models.CharField(max_length=255, null=True, blank=True)
    family = models.CharField(max_length=255)
    collection_date = models.DateField(null=True, blank=True)
    collection_data = ArrayField(models.TextField(), blank=True, null=True)
    publication_status = models.CharField(max_length=10, choices=PUBLICATION_STATUS_CHOICES, default='DRAFT')
    is_public = models.BooleanField(default=False)
    publication_date = models.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SpeciesUser', related_name='species_roles')
    habitats = models.ManyToManyField(Habitat, related_name='species', blank=True)

    # New/updated fields based on user request
    compounds = models.ManyToManyField(Compound, related_name='species', blank=True)
    references = models.ManyToManyField(Reference, related_name='species', blank=True)
    harvest_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='harvested_species')
    storage_locations = models.ManyToManyField(Location, related_name='stored_species', blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Species"

# SpeciesUser model for managing user roles per species
class SpeciesUser(models.Model):
    ROLE_CHOICES = [
        ('AUTHOR', 'Author'),
        ('CURATOR', 'Curator'),
        ('PUBLISHER', 'Publisher'),
    ]
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('species', 'user', 'role')

    def __str__(self):
        return f"{self.user.username} as {self.get_role_display()} for {self.species.name}"

# Model to store pending changes from curators
class SpeciesChange(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='changes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changes = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_changes')

    def __str__(self):
        return f"Change for {self.species.name} by {self.user.username} ({self.status})"
