from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """
    Tests for the user model
    """

    def test_create_user(self):
        """ test to create a user """
        user = User.objects.create_user(
                first_name = 'Test',
                last_name = 'User',
                email  = 'test@demo.com',
                username = 'testuser',
                password = 'testpass123'
                )
        self.assertEqual(user.email, 'test@demo.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

