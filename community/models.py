from django.db import models
from user.models import UserProfile
from cafe.models import Gallery


class Community(models.Model):
    name = models.CharField(blank=True, max_length=2000)
    owner = models.ForeignKey(UserProfile, related_name='community_owner', null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name='community_member', blank=True)
    description = models.TextField('Description')
    image = models.ForeignKey(Gallery, related_name='community', null=True, blank=True, on_delete=models.CASCADE)
    lock = models.BooleanField('Lock', default=False)

class Event(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='Event_owner', null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name='Event_member', blank=True)
    games = models.ManyToManyField(game, related_name='Event', blank=True)
    date = models.DateField()
    time = models.TimeField()
    maxMember = models.PositiveIntegerField()
    place = models.CharField(blank=True, max_length=2000)
    gallery = models.ManyToManyField(Gallery, related_name='Event', blank=True)
    plays = models.ManyToManyField(play, related_name='Event', blank=True)