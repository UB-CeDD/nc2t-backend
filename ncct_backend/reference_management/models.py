from django.db import models

class Reference(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    doi = models.CharField(max_length=255, blank=True, null=True)
    thesis_level = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

