from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("/next-word/signup")
        self.login_url = reverse("/next-word/login")
        self.logout_url = reverse("/next-word/logout")

        self.user_data = {
            "username": "testuser",
            "email": "testemail@test.ir",
            "password": "Pass123456@",
            "name": "testname",
            "age": "20",
        }

    def test_signup_endpoint(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": self.user_data["username"],
                "email": self.user_data["username"],
                "password1": self.user_data["password"],
                "password2": self.user_data["password"],
                "name": self.user_data["name"],
                "age": self.user_data["age"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_login_endpoint(self):
        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "pass": self.user_data["password"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_endpoint(self):
        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
