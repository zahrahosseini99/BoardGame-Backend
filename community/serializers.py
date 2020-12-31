from rest_framework import serializers
from . import models
from user.serializers import UserSerializer, FullUserSerializer
from cafe.serializers import CafeGallerySerializer, GameCafeSerializer
from game.models import play, game

class FullPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.play
        fields = ('id', 'players', 'semi_players', 'game', 'date', 'place', 'owner')


class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer
    members = FullUserSerializer(many=True, read_only=True, required=False)
    games = GameCafeSerializer(many=True, read_only=True, required=False)
    gallery = CafeGallerySerializer(read_only=True)
    plays = FullPlaySerializer(read_only=True)

    class Meta:
        model = models.Event
        fields = ('owner', 'members', 'games', 'date', 'time', 'maxMember', 'place', 'gallery', 'plays')
        read_only_fields = ('members', 'games', 'gallery', 'plays')


class MinusPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.play
        fields = ('id',)

        
class editEventSerializer(serializers.ModelSerializer):
    owner = UserSerializer
    members = FullUserSerializer(many=True, read_only=True, required=False)
    games = GameCafeSerializer(many=True, read_only=True, required=False)
    gallery = CafeGallerySerializer(many=True, read_only=True, required=False)
    plays = MinusPlaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = models.Event
        fields = ('owner', 'members', 'games', 'date', 'time', 'maxMember', 'place', 'gallery', 'plays')
        read_only_fields = ('members', 'games', 'gallery', 'plays')


class CommunitySerializer(serializers.ModelSerializer):
    owner = UserSerializer
    members = UserSerializer(many=True, read_only=True, required=False)
    image = CafeGallerySerializer(read_only=True)

    class Meta:
        model = models.Community
        fields = ('id', 'name', 'owner', 'members', 'description', 'image', 'lock')
        read_only_fields = ('members', 'image')


class CommunitiesListSerializer(serializers.ModelSerializer):
    owner = FullUserSerializer()
    members = FullUserSerializer(many=True, read_only=True, required=False)
    image = CafeGallerySerializer(read_only=True)

    class Meta:
        model = models.Community
        fields = ('id', 'name', 'owner', 'members', 'description', 'image', 'lock')
        read_only_fields = ('members', 'image')


