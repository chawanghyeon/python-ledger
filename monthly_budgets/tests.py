from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from monthly_budgets.models import MonthlyBudget
from users.models import User


class MonthlyBudgetViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1@user1.com", password="user1_password"
        )

        self.user1_token = RefreshToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user1_token.access_token}"
        )

        self.monthly_budget1 = MonthlyBudget.objects.create(
            user=self.user1, year=2023, month=4, budget=1000
        )

        self.monthly_budget_data = {
            "year": 2023,
            "month": 4,
            "budget": 1000,
        }

    def test_create_monthly_budget(self):
        MonthlyBudget.objects.all().delete()
        response = self.client.post(
            reverse("monthly-budgets-list"), self.monthly_budget_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            MonthlyBudget.objects.filter(
                user=self.user1,
                year=self.monthly_budget_data["year"],
                month=self.monthly_budget_data["month"],
            ).exists()
        )

    def test_retrieve_monthly_budget(self):
        response = self.client.get(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.monthly_budget1.id)
        self.assertEqual(response.data["year"], self.monthly_budget1.year)
        self.assertEqual(response.data["month"], self.monthly_budget1.month)
        self.assertEqual(response.data["budget"], f"{self.monthly_budget1.budget:.2f}")

    def test_update_monthly_budget(self):
        new_budget = 2000
        response = self.client.patch(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            ),
            {"budget": new_budget, "year": 2023, "month": 3},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["year"], 2023)
        self.assertEqual(response.data["month"], 3)
        self.assertEqual(response.data["budget"], f"{new_budget:.2f}")

    def test_delete_monthly_budget(self):
        response = self.client.delete(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            MonthlyBudget.objects.filter(
                user=self.user1,
                year=self.monthly_budget1.year,
                month=self.monthly_budget1.month,
            ).exists()
        )

    def test_list_monthly_budgets(self):
        for i in range(7):
            MonthlyBudget.objects.create(
                user=self.user1,
                year=self.monthly_budget1.year,
                month=self.monthly_budget1.month + i + 1,
                budget=self.monthly_budget1.budget,
            )

        response = self.client.get(reverse("monthly-budgets-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_monthly_budget_with_invalid_data(self):
        MonthlyBudget.objects.all().delete()
        response = self.client.post(
            reverse("monthly-budgets-list"),
            {"year": 2023, "month": 4, "budget": -1000},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(MonthlyBudget.objects.exists())

    def test_create_monthly_budget_without_authentication(self):
        MonthlyBudget.objects.all().delete()
        self.client.credentials()
        response = self.client.post(
            reverse("monthly-budgets-list"), self.monthly_budget_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(MonthlyBudget.objects.exists())

    def test_retrieve_monthly_budget_without_authentication(self):
        self.client.credentials()
        response = self.client.get(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_monthly_budget_without_authentication(self):
        self.client.credentials()
        response = self.client.patch(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            ),
            {"budget": 2000},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_monthly_budget_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(
            reverse(
                "monthly-budgets-detail",
                args=[self.monthly_budget1.id],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_monthly_budgets_without_authentication(self):
        self.client.credentials()
        response = self.client.get(reverse("monthly-budgets-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
