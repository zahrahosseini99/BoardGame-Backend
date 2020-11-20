from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from . import serializers as game_info_page_serializers
from . import serializers as play_serializer
from .models import game, play
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
        hotgames = game.objects.all().order_by('rate').reverse()[:20]
        serializer = game_info_page_serializers.GameInfoPageSerializer(hotgames, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DifficultGamesListView(generics.RetrieveAPIView):
    queryset = game.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = game_info_page_serializers.GameInfoPageSerializer

    def get(self, request):
        hotgames = game.objects.all().order_by('difficulty').reverse()[:20]
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

class SearchGameView(generics.ListAPIView):
    queryset = game.objects.all()
    serializer_class = game_info_page_serializers.GameInfoPageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class CreatePlayView(generics.CreateAPIView):
    queryset = play.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = play_serializer.playSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['owner']=user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        play = serializer.save()
        play.owner=user
        for player_data in data['players']:
            player = UserProfile.objects.all().get(username=player_data['username'])
            play.players.add(player)
        return Response("OK", status=status.HTTP_202_ACCEPTED)


class PlaysListView(generics.RetrieveUpdateAPIView):

    queryset = play.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = play_serializer.playSerializer

    def get(self, request):
        userInfo = request.user
        plays_query = userInfo.play.all()
        serializer = play_serializer.playSerializer(instance=plays_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OwnerPlaysListView(generics.RetrieveUpdateAPIView):

    queryset = play.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = play_serializer.playSerializer

    def get(self, request):
        userInfo = request.user
        plays_query = play.objects.all().filter(owner=userInfo)
        serializer = play_serializer.playSerializer(instance=plays_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditPlayView(generics.RetrieveUpdateDestroyAPIView):

    queryset = play.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = play_serializer.playSerializer

    def get(self, request, pk=None):
        user = request.user
        playInfo = play.objects.all().get(pk=pk)
        plays_query = user.play.all()
        if not plays_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = play_serializer.playSerializer(playInfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        playInfo = play.objects.all().get(pk=pk)
        plays_query = user.play.all()
        if not plays_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=playInfo, data=request.data)
        if serializer.is_valid(True):
            p = serializer.update(instance=playInfo, validated_data=serializer.validated_data)
            p.players.clear()
            for player_data in data['players']:
                player = UserProfile.objects.all().get(username=player_data['username'])
                p.players.add(player)
            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        plays_query = user.owner.all()
        print('*************', plays_query)
        if not plays_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        play = plays_query.get(pk=pk)
        play.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
