from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import serializers as community_serializer
from .models import Community
from cafe.models import Gallery
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
        data['image'] = Gallery.objects.create(base64=data['image'])
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        community = serializer.save()
        for member_id in data['members']:
            m = UserProfile.objects.get(id=member_id['username'])
            community.members.add(m)
        community.image = data['image']
        community.save()
        return Response("OK", status=status.HTTP_202_ACCEPTED)


class CommunityInfoPageView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = community_serializer.CommunitySerializer

    def get(self, request, pk=None):
        communityInfo = Community.objects.all().get(pk=pk)
        serializer = community_serializer.CommunitySerializer(communityInfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EditCommunityView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitySerializer

    def get(self, request, pk=None):
        user = request.user
        community_info = Community.objects.all().get(pk=pk)
        community_query = user.community_owner.all()
        if not community_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = community_serializer.CommunitySerializer(community_info)
        serializer.data['owner'] = UserProfile.objects.get(id=serializer.data['owner']).username
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    