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
        fields = ('id', 'name')


class PlayOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('id')


class PlayerDetailsSerializer(serializers.ModelSerializer):
    username = PlaymateSerializer

    class Meta:
        model = models.playmate
        fields = ('username', 'color', 'starting_position', 'score', 'is_won', 'is_first_time')


class playSerializer(serializers.ModelSerializer):
    players = PlayerDetailsSerializer(many=True, required=False)
    game = GamePlaySerializer()
    owner = PlayOwnerSerializer

    class Meta:
        model = models.play
        fields = ('id', 'players', 'semi_players', 'game', 'date', 'place', 'owner')
        read_only_fields = ('players', )

    def create(self, validated_data):
        playmates = validated_data.pop('players')
        instance = models.play.objects.create(**validated_data)
        for p in playmates:
            data = models.playmate.objects.create(**p)
            instance.players.add(data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.game = validated_data.get('game', instance.game)
        instance.date = validated_data.get('date', instance.date)
        instance.semi_players = validated_data.get('semi_players', instance.semi_players)
        instance.place = validated_data.get('place', instance.place)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        playmates = validated_data.get('players', instance.players)
        instance.players.all().delete()
        for p in playmates:
            new_playmate = models.playmate.objects.create(**p)
            print(new_playmate)
            instance.players.add(new_playmate)
        return instance
