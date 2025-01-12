import random
import string

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .urls import app_name


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse(f"{app_name}:signup")
        self.login_url = reverse(f"{app_name}:login")
        self.logout_url = reverse(f"{app_name}:logout")

        self.user_data = {
            "username": "testusername-".join(
                [
                    string.ascii_letters[random.randrange(0, len(string.ascii_letters))]
                    for _ in range(5)
                ]
            ),
            "email": "testemail@test.ir",
            "password": "TestPass123456@",
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

        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.url)

        self.assertEqual(follow_response.status_code, 200)
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

        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.url)

        self.assertEqual(follow_response.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_endpoint(self):
        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.url)

        self.assertEqual(follow_response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

class SuggestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.suggest_url = reverse(f"{app_name}:suggest")

        self.past_word = "سلام"
        self.suggestions = [
            ('و', 0.184397),
            ('است', 0.156028),
        ]

    def test_suggest_endpoint_with_results(self):
        response = self.client.get(self.suggest_url, {"past_word": self.past_word})
        self.assertEqual(response.status_code, 200)
        
        for (current_word, probability) in self.suggestions:
            self.assertContains(response, (current_word, probability))

    def test_suggest_endpoint_no_results(self):
        response = self.client.get(self.suggest_url, {"past_word": "اااااااا"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No suggestions available for")

    def test_suggest_endpoint_no_input(self):
        response = self.client.get(self.suggest_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Past word not provided")
