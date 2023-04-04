from rest_framework import viewsets

from monthly_budgets.models import MonthlyBudget
from monthly_budgets.serializers import MonthlyBudgetSerializer


class MonthlyBudgetViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = MonthlyBudgetSerializer
