from django.db import models


class game(models.Model):
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description')
    category = models.CharField('Category', blank=True, max_length=200)
    images = models.CharField(blank=True, max_length=2000)
    min_players = models.PositiveIntegerField(null=True)
    max_players = models.PositiveIntegerField(null=True)
    difficulty = models.FloatField(null=True)
