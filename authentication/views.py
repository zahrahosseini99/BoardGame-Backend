from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from user.models import UserProfile
from . import serializers as auth_serializers
from user import serializers as user_serializers


class RegisterView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = auth_serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        serializer_user = user_serializers.UserSerializer(user)
        tokens = serializer.data['tokens']
        data = {"refresh": tokens["refresh"], "access": tokens["access"]}
        return Response(data, status=status.HTTP_201_CREATED)
