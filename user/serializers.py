from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id','username', 'email')


class PlaymateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('username',)
