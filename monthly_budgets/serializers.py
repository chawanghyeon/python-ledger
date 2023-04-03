from rest_framework.serializers import ModelSerializer

from monthly_budgets.models import MonthlyBudget


class MonthlyBudgetSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = MonthlyBudget
        depth = 1
