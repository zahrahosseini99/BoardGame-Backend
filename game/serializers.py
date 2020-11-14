from rest_framework import serializers
from . import models
from user.serializers import PlaymateSerializer


class GameInfoPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.game
        fields = ('id', 'name', 'description', 'category', 'image', 'min_players', 'max_players', 'difficulty','rate')


class GamePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.game
        fields = ('id')


class playSerializer(serializers.ModelSerializer):
    players = PlaymateSerializer(many=True, read_only=True, required=False)
    game = GamePlaySerializer

    class Meta:
        model = models.play
        fields = ('id', 'players', 'game', 'date', 'place',)
        read_only_fields = ('players', )
