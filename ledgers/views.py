import datetime
import uuid
from datetime import timedelta
from typing import Optional

from django.http import HttpRequest
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ledgers.base62 import base62_encode
from ledgers.models import Ledger, SharedLedger
from ledgers.serializers import LedgerSerializer
from monthly_budgets.models import MonthlyBudget


class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()

    def create(self, request: HttpRequest) -> Response:
        serializer = LedgerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, type_id=request.data["type"])

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
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        queryset = Ledger.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month,
        ).order_by("-date", "-id")

        data = LedgerSerializer(queryset, many=True).data

        monthly_budget = MonthlyBudget.objects.filter(
            user=request.user, year=year, month=month
        ).first()

        if monthly_budget:
            data.data["monthly_budget"] = monthly_budget.budget

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="duplicate", url_name="duplicate")
    def duplicate_ledger(
        self, request: HttpRequest, pk: Optional[str] = None
    ) -> Response:
        ledger = Ledger.objects.get(id=pk)

        new_ledger = Ledger.objects.create(
            user=request.user,
            type=ledger.type,
            name=ledger.name,
            memo=ledger.memo,
            amount=ledger.amount,
            date=ledger.date,
        )

        return Response(
            LedgerSerializer(new_ledger).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], url_path="share", url_name="share")
    def share_ledger(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
        ledger = Ledger.objects.get(id=pk)
        expiration_date = datetime.datetime.now() + timedelta(days=1)
        shared_ledger = SharedLedger.objects.create(
            ledger=ledger, expires_at=expiration_date
        )

        encoded_token = base62_encode(uuid.uuid4().int % 10**14)

        shared_ledger.encoded_token = encoded_token
        shared_ledger.save()

        share_url = request.build_absolute_uri(
            reverse("shared-ledger", args=[encoded_token])
        )

        return Response({"url": share_url}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path="share", url_name="share")
    def delete_shared_ledger(
        self, request: HttpRequest, pk: Optional[str] = None
    ) -> Response:
        ledger = Ledger.objects.get(id=pk)
        SharedLedger.objects.filter(ledger=ledger).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedLedgerViewSet(viewsets.ViewSet):
    queryset = SharedLedger.objects.all()
    serializer_class = LedgerSerializer
    permission_classes = []

    def retrieve(self, request: HttpRequest, token: str) -> Response:
        shared_ledger = SharedLedger.objects.get(encoded_token=token)

        if shared_ledger.is_expired():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LedgerSerializer(shared_ledger.ledger)

        return Response(serializer.data, status=status.HTTP_200_OK)
