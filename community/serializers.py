from rest_framework import serializers
from . import models
from user.serializers import UserSerializer, FullUserSerializer
from cafe.serializers import CafeGallerySerializer


class CommunitySerializer(serializers.ModelSerializer):
    owner = UserSerializer
    members = UserSerializer(many=True, read_only=True, required=False)
    image = CafeGallerySerializer(read_only=True)

    class Meta:
        model = models.Community
        fields = ('name', 'owner', 'members', 'description', 'image', 'lock')
        read_only_fields = ('members', 'image')


class CommunitiesListSerializer(serializers.ModelSerializer):
    owner = FullUserSerializer()
    members = FullUserSerializer(many=True, read_only=True, required=False)
    image = CafeGallerySerializer(read_only=True)

    class Meta:
        model = models.Community
        fields = ('name', 'owner', 'members', 'description', 'image', 'lock')
        read_only_fields = ('members', 'image')
