from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from custom_types.models import CustomType
from users.models import User


class CustomTypeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1@user1.com", password="user1_password"
        )

        self.user1_token = RefreshToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user1_token.access_token}"
        )

        self.custom_type1 = CustomType.objects.create(name="test", user=self.user1)

        self.custom_type_data = {
            "name": "test",
        }

    def test_create_custom_type(self):
        CustomType.objects.all().delete()
        response = self.client.post(reverse("custom-types-list"), self.custom_type_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CustomType.objects.filter(
                name=self.custom_type_data["name"],
                user=self.user1,
            ).exists()
        )

    def test_retrieve_custom_type(self):
        response = self.client.get(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.custom_type1.name)

    def test_update_custom_type(self):
        response = self.client.patch(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            ),
            {"name": "test2"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test2")

    def test_delete_custom_type(self):
        response = self.client.delete(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            CustomType.objects.filter(
                name=self.custom_type1.name,
                user=self.user1,
            ).exists()
        )

    def test_list_custom_types(self):
        for i in range(7):
            CustomType.objects.create(
                name=f"test{i}",
                user=self.user1,
            )

        response = self.client.get(reverse("custom-types-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_custom_type_without_authentication(self):
        CustomType.objects.all().delete()
        self.client.credentials()
        response = self.client.post(reverse("custom-types-list"), self.custom_type_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(CustomType.objects.exists())

    def test_retrieve_custom_type_without_authentication(self):
        self.client.credentials()
        response = self.client.get(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_custom_type_without_authentication(self):
        self.client.credentials()
        response = self.client.patch(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            ),
            {"name": "test2"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_custom_type_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(
            reverse(
                "custom-types-detail",
                args=[self.custom_type1.name],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_custom_types_without_authentication(self):
        self.client.credentials()
        response = self.client.get(reverse("custom-types-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
