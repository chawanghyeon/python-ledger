from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response

from custom_types.models import CustomType
from custom_types.serializers import CustomTypeSerializer


class CustomTypeViewSet(viewsets.ModelViewSet):
    queryset = CustomType.objects.all()
    serializer_class = CustomTypeSerializer

    def create(self, request: HttpRequest) -> Response:
        if CustomType.objects.filter(
            user=request.user, name=request.data["name"]
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request: HttpRequest) -> Response:
        queryset = CustomType.objects.filter(user=request.user).order_by("name")

        paginator = self.paginator
        paginator.ordering = "name"
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomTypeSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
