from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ledgers.models import Ledger
from ledgers.serializers import LedgerSerializer


class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()

    def create(self, request: HttpRequest) -> Response:
        serializer = LedgerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, type_id=request.data["type_id"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: HttpRequest) -> Response:
        queryset = Ledger.objects.filter(user=request.user).order_by("-date", "-id")

        paginator = self.paginator
        paginator.ordering = "-date", "-id"
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LedgerSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"], url_path="date", url_name="date")
    def get_monthly_ledgers(self, request: HttpRequest) -> Response:
        queryset = Ledger.objects.filter(
            user=request.user,
            date__year=request.query_params["year"],
            date__month=request.query_params["month"],
        ).order_by("-date", "-id")

        paginator = self.paginator
        paginator.ordering = "-date", "-id"
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LedgerSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
