from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='adminuser@demo.com',
            username='adminuser',
            password='adminpass',
            first_name='Admin',
            last_name='User'
        )
        self.normal_user = User.objects.create_user(
            email='normaluser@demo.com',
            username='normaluser',
            password='userpass',
            first_name='Normal',
            last_name='User'
        )
        self.user_list_url = reverse('user-list')
        self.user_me_url = reverse('user-me')
        self.user_detail_url = lambda uid: reverse('user-detail', kwargs={'user_id': uid})


    def test_unauthenticated_user_cannot_view_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_only_admin_can_view_user_list(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', [])
        self.assertIn(self.normal_user.email, [user['email'] for user in results])


    def test_anyone_can_create_user(self):
        data = {
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@demo.com",
            "username": "newuser",
            "password": "newuserpass"
        }
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_access_me_endpoint(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.normal_user.email)


    def test_admin_can_retrieve_update_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        detail_url = self.user_detail_url(self.normal_user.user_id)

        # Retrieve
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update
        response = self.client.patch(detail_url, {"username": "updateduser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")

        # Delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_non_admin_cannot_access_other_users(self):
        self.client.force_authenticate(user=self.normal_user)
        detail_url = self.user_detail_url(self.admin_user.user_id)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)