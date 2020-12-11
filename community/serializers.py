from rest_framework import serializers
from . import models
from user.models import UserProfile
from cafe.models import Gallery


class CommunitySerializer(serializers.ModelSerializer):
    owner = UserProfile
    members = UserProfile(many=True, required=False)
    image = Gallery

    class Meta:
        model = models.Community
        fields = ('name', 'owner', 'members', 'description', 'image', 'lock')
