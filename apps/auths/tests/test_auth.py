from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.users.models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('auth-signup')
        self.login_url = reverse('auth-login')
        self.user_data = {
            "email": "testcase@demo.com",
            "username": "testcase",
            "first_name": "Test",
            "last_name": "Case",
            "password": "testcase123"
        }

    def test_user_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().email, self.user_data["email"])

    def test_user_signup_with_existing_email(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_with_wrong_password(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        login_data = {
            "email": self.user_data["email"],
            "password": "a_wrongpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_non_existent_user_details(self):
        login_data = {
            "email": "stranguser@demo.com",
            "password": "a_password"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
