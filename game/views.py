from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import serializers as game_info_page_serializers
from .models import game


class GameInfoPageView(generics.RetrieveAPIView):
    queryset = game.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = game_info_page_serializers.GameInfoPageSerializer

    def get(self, request, pk=None):
        gameInfo = game.objects.all().get(pk=pk)
        serializer = game_info_page_serializers.GameInfoPageSerializer(gameInfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
