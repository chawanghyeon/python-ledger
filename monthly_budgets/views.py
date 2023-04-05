from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response

from monthly_budgets.models import MonthlyBudget
from monthly_budgets.serializers import MonthlyBudgetSerializer


class MonthlyBudgetViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = MonthlyBudgetSerializer

    def create(self, request: HttpRequest) -> Response:
        if MonthlyBudget.objects.filter(
            user=request.user,
            year=request.data["year"],
            month=request.data["month"],
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = MonthlyBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request: HttpRequest) -> Response:
        queryset = MonthlyBudget.objects.filter(user=request.user).order_by(
            "-year", "-month"
        )

        paginator = self.paginator
        paginator.ordering = "-year", "-month"
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MonthlyBudgetSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
