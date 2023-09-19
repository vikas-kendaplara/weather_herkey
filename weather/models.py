from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30)
    location_key = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'