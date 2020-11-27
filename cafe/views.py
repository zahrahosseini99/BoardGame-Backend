from django.shortcuts import render
from . import serializers as cafe_serializer
from .models import Cafe
from user.models import UserProfile
from game.models import game


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