from django.db import models
from user.models import UserProfile


class game(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description')
    category = models.CharField('Category', blank=True, max_length=200)
    image = models.CharField(null=True, max_length=2000)
    min_players = models.PositiveIntegerField(null=True)
    max_players = models.PositiveIntegerField(null=True)
    difficulty = models.FloatField(null=True)
    rate = models.FloatField(null=True)


class play(models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(UserProfile, related_name='play', blank=True)
    game = models.ForeignKey(game, related_name='play', on_delete=models.CASCADE)
    date = models.DateField()
    place = models.CharField(blank=True, max_length=2000)
