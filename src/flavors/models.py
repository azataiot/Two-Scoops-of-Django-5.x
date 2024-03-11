# flavors/models.py
from django.db import models

# Create your models here.

from core.models import TimeStampedModel


class Flavor(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
