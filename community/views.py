from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from . import serializers as community_serializer
from .models import Community, Event
from game.models import play, game
from cafe.models import Gallery
from user.models import UserProfile
import random
import datetime

class SearchCommunityView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = community_serializer.CommunitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', 'description']


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
    serializer_class = community_serializer.CommunitiesListSerializer

    def get(self, request, pk=None):
        communityInfo = Community.objects.all().get(pk=pk)
        serializer = community_serializer.CommunitiesListSerializer(communityInfo)
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


    def put(self, request, pk=None):
        user = request.user
        data = request.data
        community_info = Community.objects.all().get(pk=pk)
        community_query = user.community_owner.all()

        community_info.image = Gallery.objects.create(base64=data['image'])

        if not community_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=community_info, data=data)
        if serializer.is_valid(True):
            community = serializer.update(instance=community_info, validated_data=serializer.validated_data)
            community.members.clear()
            for member_id in data['members']:
                m = UserProfile.objects.get(username=member_id['username'])
                community.members.add(m)
            community.events.clear()
            for event_id in data['events']:
                e = Event.objects.get(id=event_id['id'])
                community.events.add(e)
            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        community_info = Community.objects.all().get(pk=pk)
        community_query = user.community_owner.all()
        if not community_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        events_info = community_info.events.all()
        for e in events_info:
            e.delete()
        community_info.delete()
        return Response("OK", status=status.HTTP_202_ACCEPTED)


class CommunitiesListView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = community_serializer.CommunitiesListSerializer

    def get(self, request):
        communitiesList = Community.objects.all()
        serializer = community_serializer.CommunitiesListSerializer(communitiesList, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OwnerCommunitiesListView(generics.RetrieveAPIView):

    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitiesListSerializer

    def get(self, request):
        user = request.user
        communities_query = user.community_owner.all()
        serializer = community_serializer.CommunitiesListSerializer(communities_query, many=True)
        for community in serializer.data:
            community['owner'] = UserProfile.objects.get(username=community['owner']['username']).username
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberCommunitiesListView(generics.RetrieveAPIView):

    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitiesListSerializer

    def get(self, request):
        user = request.user
        communities_query = user.community_member.all()
        serializer = community_serializer.CommunitiesListSerializer(communities_query, many=True)
        for community in serializer.data:
            community['owner'] = UserProfile.objects.get(username=community['owner']['username']).username
        return Response(serializer.data, status=status.HTTP_200_OK)


class RandomCommunitiesListView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = community_serializer.CommunitiesListSerializer

    def get(self, request):
        communities_list = list(Community.objects.all())
        if len(communities_list) > 20 :
            serializer = community_serializer.CommunitiesListSerializer(random.sample(communities_list, 20), many=True)
        else:
            serializer = community_serializer.CommunitiesListSerializer(communities_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JoinCommunityView(generics.UpdateAPIView):
    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitySerializer

    def put(self, request, pk=None):
        user = request.user
        community_info = Community.objects.get(pk=pk)
        if community_info.lock:
            return Response("The community is lock", status=status.HTTP_400_BAD_REQUEST)
        if community_info.members.all().filter(id=user.id).exists():
            return Response("User has already joined", status=status.HTTP_400_BAD_REQUEST)
        community_info.members.add(user)
        return Response("ok!", status=status.HTTP_200_OK)


class LeaveCommunityView(generics.UpdateAPIView):
    queryset = Community.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.CommunitySerializer

    def put(self, request, pk=None):
        user = request.user
        community_info = Community.objects.get(pk=pk)
        if not community_info.members.all().filter(id=user.id).exists():
            return Response("This user does not exist in community", status=status.HTTP_400_BAD_REQUEST)
        community_info.members.remove(user)
        return Response("ok!", status=status.HTTP_200_OK)


class CreateEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.EventSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        for member in data['members']:
            member['username'] = UserProfile.objects.get(username=member['username']).id
        max_members = data['maxMember']
        if len(data['members']) > max_members:
            return Response("too many members,change the limitation", status=status.HTTP_400_BAD_REQUEST)
        data['owner'] = user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        event = serializer.save()
        for member_id in data['members']:
            m = UserProfile.objects.get(id=member_id['username'])
            event.members.add(m)
        for game_id in data['games']:
            g = game.objects.get(id=game_id['id'])
            event.games.add(g)
        for image_id in data['gallery']:
            i = Gallery.objects.create(base64=image_id['base64'])
            event.gallery.add(i)
        event.save()
        c = Community.objects.get(id=data['community']['id'])
        c.events.add(event)
        c.save()
        return Response("OK", status=status.HTTP_202_ACCEPTED)

class JoinEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.EventSerializer

    def put(self, request, pk=None):
        user = request.user
        event_info = Event.objects.get(pk=pk)
        if event_info.members.count()==event_info.maxMember:
            return Response("The event is full", status=status.HTTP_400_BAD_REQUEST)
        mydate = datetime.date.today()
        mytime = datetime.datetime.now()
        if mydate >= event_info.date:
            return Response("finished", status=status.HTTP_400_BAD_REQUEST)
        elif mydate == event_info.date:
            if mytime >= event_info.time:
                return Response("finished", status=status.HTTP_400_BAD_REQUEST)
        if event_info.members.all().filter(id=user.id).exists():
            return Response("User has already joined", status=status.HTTP_400_BAD_REQUEST)
        event_info.members.add(user)
        return Response("ok!", status=status.HTTP_200_OK)

class LeaveEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.EventSerializer

    def put(self, request, pk=None):
        user = request.user
        event_info = Event.objects.get(pk=pk)
        if not event_info.members.all().filter(id=user.id).exists():
            return Response("This user does not exist in event", status=status.HTTP_400_BAD_REQUEST)
        event_info.members.remove(user)
        return Response("ok!", status=status.HTTP_200_OK)


class EditEventView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = community_serializer.editEventSerializer

    def get(self, request, pk=None):
        user = request.user
        event_info = Event.objects.get(pk=pk)
        event_query = user.Event_owner.all()
        if not event_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = community_serializer.editEventSerializer(event_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        event_info = Event.objects.get(pk=pk)
        event_query = user.Event_owner.all()

        if not event_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=event_info, data=data)
        if serializer.is_valid(True):
            event = serializer.update(instance=event_info, validated_data=serializer.validated_data)
            event.members.clear()
            for member_id in data['members']:
                m = UserProfile.objects.get(username=member_id['username'])
                event.members.add(m)

            event.gallery.clear()
            for image_id in data['gallery']:
                i = Gallery.objects.create(base64=image_id['base64'])
                event.gallery.add(i)

            event.games.clear()
            for game_id in data['games']:
                g = game.objects.get(id=game_id['id'])
                event.games.add(g)

            event.plays.clear()
            for play_id in data['plays']:
                p = play.objects.get(id=play_id['id'])
                event.plays.add(p)

            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        event_info = Event.objects.all().get(pk=pk)
        event_query = user.Event_owner.all()
        if not event_query.filter(pk=pk).exists():
            return Response("Bad Request!!", status=status.HTTP_400_BAD_REQUEST)
        gallery_info = event_info.gallery.all()
        for i in gallery_info:
            i.delete()
        event_info.delete()
        return Response("OK", status=status.HTTP_202_ACCEPTED)
