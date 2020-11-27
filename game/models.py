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


class playmate(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    color = models.CharField('Color', max_length=200, blank=True)
    starting_position = models.CharField('Starting position', max_length=200, blank=True)
    score = models.CharField('Score', max_length=200, blank=True)
    is_won = models.BooleanField('Is won', default=False)
    is_first_time = models.BooleanField('Is first time', default=False)


class play(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(UserProfile, related_name='owner', null=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(playmate, related_name='play', blank=True)
    semi_players = models.CharField(blank=True, max_length=2000)
    game = models.ForeignKey(game, related_name='play', on_delete=models.CASCADE)
    date = models.DateField()
    place = models.CharField(blank=True, max_length=2000)
