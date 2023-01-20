from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    def __repr__(self):
        return f'{self.name} {self.latitude} {self.longitude}'
    def __str__(self):
        return f'{self.name} {self.latitude} {self.longitude}'

class AccountHolder(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    cities_visited = models.ManyToManyField(City)
    def __str__(self):
        return self.user.username
    def __repr__(self):
        return self.user.username

