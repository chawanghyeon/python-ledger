from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import UntypedToken

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

    def retrieve(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
        jwt_auth = JWTAuthentication()

        try:
            user, jwt = jwt_auth.authenticate(request)
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
        user = authenticate(
            username=request.user.username, password=request.data.get("password")
        )

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_name="signin")
    def signin(self, request: HttpRequest) -> Response:
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        token = TokenObtainPairSerializer().validate(data)
        user = authenticate(**data)
        serializer = UserSerializer(user)

        return Response(
            {
                "user": serializer.data,
                "message": "Login successfully",
                "token": {"refresh": token["refresh"], "access": token["access"]},
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_name="signout")
    def signout(self, request: HttpRequest) -> Response:
        raw_token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]

        try:
            json_token_id = UntypedToken(raw_token)["jti"]
        except TokenError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        BlacklistedToken.objects.create(jti=json_token_id)

        return Response(status=status.HTTP_200_OK)
