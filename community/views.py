from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as community_serializer
from .models import Community
from user.models import UserProfile


class CreateCommunityView(generics.CreateAPIView):
    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitySerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        for member in data['members']:
            member['username'] = UserProfile.objects.get(username=member['username']).id
        data['owner'] = user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        community = serializer.save()
        for member_id in data['members']:
            m = UserProfile.objects.get(id=member_id['username'])
            community.members.add(m)
        return Response("OK", status=status.HTTP_202_ACCEPTED)
