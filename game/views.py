from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from . import serializers as game_info_page_serializers
from .models import game
from user.models import UserProfile
from user.serializers import UserSerializer


class GameInfoPageView(generics.RetrieveAPIView):
    queryset = game.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = game_info_page_serializers.GameInfoPageSerializer

    def get(self, request, pk=None):
        gameInfo = game.objects.all().get(pk=pk)
        serializer = game_info_page_serializers.GameInfoPageSerializer(gameInfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HotnessGamesListView(generics.RetrieveAPIView):
    queryset = game.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = game_info_page_serializers.GameInfoPageSerializer

    def get(self, request):
        hotgames = game.objects.all().order_by('rate').reverse()[:5]
        serializer = game_info_page_serializers.GameInfoPageSerializer(hotgames, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GamesListView(generics.RetrieveAPIView):
    queryset = game.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = game_info_page_serializers.GameInfoPageSerializer

    def get(self, request):
        gamesList=game.objects.all().order_by('rate').reverse()
        serializer = game_info_page_serializers.GameInfoPageSerializer(gamesList,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchUserView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username']