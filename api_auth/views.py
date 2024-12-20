from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.serializers import UserDetailSerializer, UserSerializer

# Create your views here.


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]


class LoginView(APIView):

    def post(self, request: Response):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user and isinstance(user, User):
            refresh: RefreshToken = RefreshToken.for_user(user)  # type:ignore
            context = {
                "status": "success",
                "content": {
                    "username": username,
                    "first_name": user.first_name,
                    "token": str(refresh.access_token),
                },
            }
        else:
            context = {
                "status": "error",
                "content": "Incorrect credencials",
            }
        return Response(context)


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get("lookup_value")

        try:
            obj = queryset.get(id=lookup_value)
        except (User.DoesNotExist, ValueError):
            obj = get_object_or_404(queryset, username=lookup_value)
        return obj
