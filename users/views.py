from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request: HttpRequest) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            password=make_password(request.data.get("password")), is_active=True
        )

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_name="me")
    def retrieve_me(self, request: HttpRequest) -> Response:
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
        user = authenticate(
            username=request.user.username, password=request.data.get("password")
        )

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_name="signin")
    def signin(self, request: HttpRequest) -> Response:
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        user = authenticate(**data)

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        token = RefreshToken.for_user(user)
        serializer = UserSerializer(user)

        return Response(
            {
                "user": serializer.data,
                "message": "Login successfully",
                "token": {"refresh": str(token), "access": str(token.access_token)},
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_name="signout")
    def signout(self, request: HttpRequest) -> Response:
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
