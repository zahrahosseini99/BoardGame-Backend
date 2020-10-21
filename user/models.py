from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(null=True)
