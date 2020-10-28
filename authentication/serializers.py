from django.utils.six import text_type
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework import status

class RegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'username', 'password', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = text_type(tokens)
        access = text_type(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

    def create(self, validated_data):
        return models.UserProfile.objects.create_user(username=validated_data.get("username"),
                                                      email=validated_data.get("email"),
                                                      password=validated_data.get("password"))
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id

        return token


class EditProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'avatar','age')
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True},
        # }

    def validate_email(self, value):
        user = self.context['request'].user
        if models.UserProfile.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.avatar = validated_data['avatar']
        instance.age = validated_data['age']

        # instance.username = validated_data['username']

        instance.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.UserProfile
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()
        return instance,Response("changed!!!", status=status.HTTP_201_CREATED)
