from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    def __repr__(self):
        return self.name + " " + self.latitude + " " + self.longitude
    def __str__(self):
        return self.name + " " + self.latitude + " " + self.longitude

