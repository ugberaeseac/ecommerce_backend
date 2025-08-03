from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('auth-signup')
        self.login_url = reverse('auth-login')
        self.logout_url = reverse('auth-logout')

        self.user_data = {
            "email": "testcase@demo.com",
            "username": "testcase",
            "first_name": "Test",
            "last_name": "Case",
            "password": "testcase123"
        }

        self.normal_user = User.objects.create_user(**self.user_data)
        self.refresh_token = RefreshToken.for_user(self.normal_user)
        self.access_token = str(self.refresh_token.access_token)

    def test_user_signup_success(self):
        User.objects.all().delete()
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().email, self.user_data["email"])

    def test_user_signup_with_existing_email(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_with_wrong_password(self):
        login_data = {
            "email": self.user_data["email"],
            "password": "a_wrongpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_non_existent_user_details(self):
        login_data = {
            "email": "strangeuser@demo.com",
            "password": "a_password"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.logout_url, {'refresh': str(self.refresh_token)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn('detail', response.data)

    def test_unauthenticated_user_cannot_logout(self):
        self.client.credentials()
        response = self.client.post(self.logout_url, {'refresh': str(self.refresh_token)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)