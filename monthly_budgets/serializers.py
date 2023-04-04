from rest_framework.serializers import ModelSerializer

from monthly_budgets.models import MonthlyBudget


class MonthlyBudgetSerializer(ModelSerializer):
    class Meta:
        exclude = ("user",)
        model = MonthlyBudget
        depth = 1
