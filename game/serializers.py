from rest_framework import serializers
from . import models


class GameInfoPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.game
        fields = ('id', 'name', 'description', 'category', 'image', 'min_players', 'max_players', 'difficulty','rate')
