from django.db import models
from user.models import UserProfile
from cafe.models import Gallery

# Create your models here.

class Community(models.Model):
    name = models.CharField(blank=True, max_length=2000)
    owner = models.ForeignKey(UserProfile, related_name='owner', null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name='Community', blank=True)
    description = models.TextField('Description')
    image = models.ForeignKey(Gallery, related_name='Community', blank=True, on_delete=models.CASCADE)
    lock = models.BooleanField('Lock', default=False)
   