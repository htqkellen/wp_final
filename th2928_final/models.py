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

class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    weather = models.CharField(max_length=50)
    update_date = models.DateField()
    def __repr__(self):
        return f'{self.city.name} {self.weather} {self.update_date}'
    def __str__(self):
        return f'{self.city.name} {self.weather} {self.update_date}'

class State(models.Model):
    name = models.CharField(max_length=100)
    postal = models.CharField(max_length=5)
    abb = models.CharField(max_length=50)
    def __repr__(self):
        return f'{self.name} {self.abb} {self.postal}'
    def __str__(self):
        return f'{self.name} {self.abb} {self.postal}'

class AccountHolder(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    cities_visited = models.ManyToManyField(City)

    def __str__(self):
        return self.user.username
    def __repr__(self):
        return self.user.username

