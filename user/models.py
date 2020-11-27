from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    avatar = models.CharField(blank=True, max_length=500000)
    age = models.PositiveIntegerField(null=True)
    
    class Meta(object):
        unique_together = ('email',)
