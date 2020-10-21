from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import UserProfile
from . import serializers


class UserList(generics.ListAPIView):
    permission_class = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()

