from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.serializers import UserSerializer

# from rest_framework.authentication import \
#    TokenAuthentication  # BaseAuthentication, SessionAuthentication,

# Create your views here.


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


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
                    "full_name":
                        f"{user.first_name} {user.last_name}",
                    "token": str(refresh.access_token),
                }
            }
        else:
            context = {
                "status": "error",
                "content": "Incorrect credencials",
            }

        return Response(context)
