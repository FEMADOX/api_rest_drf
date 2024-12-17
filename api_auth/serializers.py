from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "first_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "first_name", "password"]


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        if user and isinstance(user, User):
            token = super().get_token(user)
            token["username"] = user.username
            token["first_name"] = user.first_name

            return token
