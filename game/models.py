from django.db import models


class game(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description')
    category = models.CharField('Category', blank=True, max_length=200)
    image = models.CharField(blank=True, max_length=2000)
    min_players = models.PositiveIntegerField(null=True)
    max_players = models.PositiveIntegerField(null=True)
    difficulty = models.FloatField(null=True)
    rate = models.FloatField(null=True)
