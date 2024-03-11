from django.db import models


# Create your models here.


class Tasting(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tastings')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
