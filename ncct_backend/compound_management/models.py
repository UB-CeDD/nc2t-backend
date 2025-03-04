from django.db import models

# Compound model
class Compound(models.Model):
    subclass = models.CharField(max_length=255, primary_key=True)
    compound_class = models.CharField(max_length=255)
    smiles = models.TextField()

    def __str__(self):
        return f"Compound {self.subclass}"