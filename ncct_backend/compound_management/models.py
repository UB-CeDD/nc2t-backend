import uuid
import secrets

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.exceptions import ValidationError

# Function to generate a random string
def generate_unique_id():
    return secrets.token_urlsafe(16)

class Compound(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    other_names = ArrayField(models.TextField(), blank=True, null=True)
    pubchem_id = models.CharField(max_length=255, null=True, blank=True)
    bio_activity = models.CharField(null=True, blank=True)
    subclass = models.CharField(max_length=255)
    compound_class = models.CharField(max_length=255)
    smiles = models.TextField(unique=True)

    def clean(self):
        super().clean()
        if self.smiles:
            existing_compound = Compound.objects.filter(smiles=self.smiles).exclude(pk=self.pk).first()
            if existing_compound:
                raise ValidationError(f"A compound with the SMILES string '{self.smiles}' already exists (subclass: {existing_compound.subclass}).")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compound {self.subclass}"

