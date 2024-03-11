# promos/models.py

from django.db import models


class Promo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='promos')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
