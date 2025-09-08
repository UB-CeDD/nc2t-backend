import uuid
import secrets
from django.db import models

# Function to generate a random string
def generate_unique_id():
    return secrets.token_urlsafe(16)

class Reference(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=generate_unique_id, editable=False, unique=True)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    doi = models.CharField(max_length=255, blank=True, null=True)
    thesis_level = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

