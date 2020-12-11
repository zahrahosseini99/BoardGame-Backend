from rest_framework import serializers
from . import models
from user.models import UserProfile



class GameCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.game
        fields = ('id', 'name','image')


class CafeOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', )

class CafeGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gallery
        fields = ('id','base64')


class CafeSerializer(serializers.ModelSerializer):
    games = GameCafeSerializer(many=True, read_only=True, required=False)
    owner = CafeOwnerSerializer
    gallery = CafeGallerySerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Cafe
        fields = ('id', 'name', 'owner', 'description', 'games', 'price', 'open_time', 'close_time', 'phone_number', 'gallery', 'city', 'latitude', 'longitude')
        read_only_fields = ('games', )
