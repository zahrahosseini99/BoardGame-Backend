from django.db import models
from user.models import UserProfile
from game.models import game

class Cafe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)
    owner = models.ForeignKey(UserProfile, related_name='Cafe', null=True, on_delete=models.CASCADE)
    description = models.TextField('Description', blank=True)
    games = models.ManyToManyField(game, related_name='Cafe', blank=True)
    price = models.TextField('Price', blank=True)
    open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    phone_number = models.CharField(blank=True, max_length=20)
    gallery = models.TextField('Gallery', blank=True)
    city = models.CharField(blank=True, max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)