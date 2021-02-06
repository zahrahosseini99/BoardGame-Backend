from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from . import serializers as cafe_serializer
from .models import Cafe,Gallery
from user.models import UserProfile
from game.models import game
import random


class CafeInfoPageView(generics.RetrieveAPIView):
    queryset = Cafe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = cafe_serializer.CafeSerializer

    def get(self, request, pk=None):
        cafeInfo = Cafe.objects.all().get(pk=pk)
        serializer = cafe_serializer.CafeSerializer(cafeInfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        for image_id in data['gallery']:
            i = Gallery.objects.create(base64=image_id['base64'])
            cafe.gallery.add(i)
        return Response("OK", status=status.HTTP_202_ACCEPTED)


class CafeListView(generics.RetrieveAPIView):
    queryset = Cafe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = cafe_serializer.CafeSerializer

    def get(self, request):
        cafeList = Cafe.objects.all()
        serializer = cafe_serializer.CafeSerializer(cafeList, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class RandomCafeListView(generics.RetrieveAPIView):
    queryset = Cafe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = cafe_serializer.CafeSerializer

    def get(self, request):
        cafe_list = list(Cafe.objects.all())
        if len(cafe_list) > 20 :
            serializer = cafe_serializer.CafeSerializer(random.sample(cafe_list, 20), many=True)
        else:
            serializer = cafe_serializer.CafeSerializer(cafe_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EditCafeView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Cafe.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = cafe_serializer.CafeSerializer

    def get(self, request, pk=None):
        user = request.user
        cafe_info = Cafe.objects.all().get(pk=pk)
        cafes_query = user.Cafe.all()
        if not cafes_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = cafe_serializer.CafeSerializer(cafe_info)
        serializer.data['owner'] = UserProfile.objects.get(id=serializer.data['owner']).username
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        cafe_info = Cafe.objects.all().get(pk=pk)
        cafes_query = user.Cafe.all()
        if not cafes_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=cafe_info, data=data)
        if serializer.is_valid(True):
            cafe = serializer.update(instance=cafe_info, validated_data=serializer.validated_data)
            cafe.games.clear()
            for game_id in data['games']:
                g = game.objects.get(id=game_id['id'])
                cafe.games.add(g)
                
            cafe.gallery.clear()
            for image_id in data['gallery']:
                i = Gallery.objects.create(base64=image_id['base64'])
                cafe.gallery.add(i)
            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        cafe_info = Cafe.objects.all().get(pk=pk)
        cafes_query = user.Cafe.all()
        if not cafes_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        gallery_info = cafe_info.gallery.all()
        for i in gallery_info:
            i.delete()
        cafe_info.delete()
        return Response("OK", status=status.HTTP_202_ACCEPTED)
