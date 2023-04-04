from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1@user1.com", password="user1_password"
        )

        self.user_data = {
            "username": "user1@user1.com",
            "password": "user1_password",
            "is_active": "True",
        }

        user1_token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_token}")

    def test_create_user(self):
        User.objects.all().delete()
        self.client.credentials()
        response = self.client.post(reverse("users-list"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_create_user_wrong_username(self):
        User.objects.all().delete()
        self.client.credentials()
        self.user_data["username"] = "wrongusername"
        response = self.client.post(reverse("users-list"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_signin(self):
        response = self.client.post(reverse("users-signin"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("access", response.data["token"])
        self.assertIn("refresh", response.data["token"])
        self.assertTrue(response.data["user"]["username"], self.user_data["username"])

    def test_signin_wrong_credentials(self):
        self.user_data["password"] = "wrongpassword"
        response = self.client.post(reverse("users-signin"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        response = self.client.get(reverse("users-detail", args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserSerializer(self.user1)
        self.assertEqual(response.data, serializer.data)

    def test_destroy_user(self):
        response = self.client.delete(
            reverse("users-detail", args=[self.user1.id]),
            {"password": "user1_password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_destroy_user_wrong_password(self):
        response = self.client.delete(
            reverse("users-detail", args=[self.user1.id]), {"password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_without_authentication(self):
        self.client.credentials()
        response = self.client.get(reverse("users-detail", args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_user_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(
            reverse("users-detail", args=[self.user1.id]),
            {"password": "user1_password"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
