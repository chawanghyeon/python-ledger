from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.response import Response

from monthly_budgets.models import MonthlyBudget
from monthly_budgets.serializers import MonthlyBudgetSerializer


class MonthlyBudgetViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = MonthlyBudgetSerializer

    def create(self, request: HttpRequest) -> Response:
        serializer = MonthlyBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)
