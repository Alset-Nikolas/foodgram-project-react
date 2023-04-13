from django.test import TestCase
from users.models import User


class TaskModelTest(TestCase):
    def test_create_valid_user(self):
        email = "ah@gmail.com"
        password = "testpass1"
        username = "user_name"
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
