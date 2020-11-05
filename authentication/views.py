from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from user.models import UserProfile
from . import serializers as auth_serializers
from user import serializers as user_serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated


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
        data = {"refresh": tokens["refresh"], "access": tokens["access"], "id": serializer_user.data["id"]}
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
        Get Refresh And Access Token by Username and Password Given
    """
    serializer_class = auth_serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            user = UserProfile.objects.get(username=request.data['username'])
        except ObjectDoesNotExist:
            data = dict()
            data["non_field_errors"] = ["Either the username or entry doesn't exist."]
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.validated_data['id'] = user.id
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileView(generics.RetrieveUpdateAPIView):

    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = auth_serializers.EditProfileSerializer

    def get(self, request):
        userInfo = request.user
        serializer = auth_serializers.EditProfileSerializer(instance=userInfo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        userInfo = request.user
        data = request.data
        serializer = self.get_serializer(instance=userInfo, data=data)
        if serializer.is_valid(True):
            serializer.update(instance=userInfo, validated_data=serializer.validated_data)
            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = auth_serializers.ChangePasswordSerializer

    def put(self, request):
        userInfo = request.user
        data = request.data
        serializer = self.get_serializer(instance=userInfo, data=data)
        if serializer.is_valid(True):
            serializer.update(instance=userInfo, validated_data=serializer.validated_data)
            return Response("OK", status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)
