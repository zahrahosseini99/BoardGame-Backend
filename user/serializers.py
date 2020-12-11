from rest_framework import serializers
from . import models


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'avatar', 'age')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id','username', 'email')


class PlaymateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('username',)
