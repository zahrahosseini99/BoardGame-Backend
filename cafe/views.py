from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from . import serializers as cafe_serializer
from .models import Cafe
from user.models import UserProfile
from game.models import game


class SearchCafeView(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = cafe_serializer.CafeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class CreateCafeView(generics.CreateAPIView):
    queryset = Cafe.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = cafe_serializer.CafeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['owner'] = user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        cafe = serializer.save()
        for game_id in data['games']:
            g = game.objects.get(id=game_id['id'])
            cafe.games.add(g)
        return Response("OK", status=status.HTTP_202_ACCEPTED)


class OwnerCafesListView(generics.RetrieveAPIView):

    queryset = Cafe.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = cafe_serializer.CafeSerializer

    def get(self, request):
        user = request.user
        cafes_query = user.Cafe.all()
        serializer = cafe_serializer.CafeSerializer(cafes_query, many=True)
        print(serializer.data)
        for cafe in serializer.data:
            cafe['owner'] = UserProfile.objects.get(id=cafe['owner']).username
        return Response(serializer.data, status=status.HTTP_200_OK)
