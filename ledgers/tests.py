from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from custom_types.models import CustomType
from ledgers.models import Ledger
from users.models import User


class LedgerViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1@user1.com", password="user1_password"
        )

        self.user1_token = RefreshToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user1_token.access_token}"
        )

        self.type1 = CustomType.objects.create(user=self.user1, name="type1")

        self.ledger_data = {
            "user_id": self.user1.id,
            "name": "ledger1",
            "memo": "memo1",
            "amount": 1000,
            "type_id": self.type1.id,
            "date": "2023-04-04",
        }

        self.ledger1 = Ledger.objects.create(**self.ledger_data)

    def test_create_ledger(self):
        Ledger.objects.all().delete()
        response = self.client.post(
            reverse("ledgers-list"), self.ledger_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ledger.objects.count(), 1)
        self.assertEqual(response.data["name"], "ledger1")

    def test_retrieve_ledger(self):
        response = self.client.get(reverse("ledgers-detail", args=[self.ledger1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.ledger1.name)

    def test_update_ledger(self):
        response = self.client.patch(
            reverse("ledgers-detail", args=[self.ledger1.id]),
            {"name": "ledger2", "memo": "memo2", "amount": 2000},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "ledger2")
        self.assertEqual(response.data["memo"], "memo2")
        self.assertEqual(response.data["amount"], f"{2000:.2f}")

    def test_delete_ledger(self):
        response = self.client.delete(reverse("ledgers-detail", args=[self.ledger1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ledger.objects.count(), 0)
