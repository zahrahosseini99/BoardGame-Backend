from rest_framework import serializers
from . import models
from user.models import UserProfile
from user.serializers import PlaymateSerializer


class GameInfoPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.game
        fields = ('id', 'name', 'description', 'category', 'image', 'min_players', 'max_players', 'difficulty','rate')


class GamePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.game
        fields = ('id')

class PlayOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('id')


class playSerializer(serializers.ModelSerializer):
    players = PlaymateSerializer(many=True, read_only=True, required=False)
    game = GamePlaySerializer
    owner = PlayOwnerSerializer
    class Meta:
        model = models.play
        fields = ('id', 'players', 'game', 'date', 'place','owner',)
        read_only_fields = ('players', )
