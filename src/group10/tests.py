import random
import string

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .urls import app_name


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.csrf_url = reverse(f"{app_name}:csrf")
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
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        csrf_token = response.json()["csrf"]

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
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_login_endpoint(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        csrf_token = response.json()["csrf"]

        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "pass": self.user_data["password"],
            },
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
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


class SuggestTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testusername-".join(
                [
                    string.ascii_letters[random.randrange(0, len(string.ascii_letters))]
                    for _ in range(5)
                ]
            ),
            "password": "TestPass123456@",
        }

        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        self.client = Client()
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )

        self.suggest_url = reverse(f"{app_name}:suggest")
        self.learn_url = reverse(f"{app_name}:learn")
        self.past_word1 = "حافظ"
        self.suggestion1 = "شیرازی"
        self.past_word2 = "حافظ"
        self.suggestion2 = "دروازه"
        self.bad_word = "اااااااا"

    def test_suggest_endpoint_with_results(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        csrf_token = response.json()["csrf"]

        response = self.client.get(
            self.suggest_url,
            {"past_word": self.past_word1},
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("suggestions", data)
        self.assertNotEqual(len(data["suggestions"]), 0)

        self.assertEqual(self.suggestion1 in data["suggestions"], True)

    def test_suggest_endpoint_with_no_results(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        csrf_token = response.json()["csrf"]

        response = self.client.get(
            self.suggest_url,
            {"past_word": self.bad_word},
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("suggestions", data)
        self.assertEqual(len(data["suggestions"]), 0)

    def test_suggest_endpoint_with_no_past_word(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        csrf_token = response.json()["csrf"]

        response = self.client.get(
            self.suggest_url,
            {"past_word": ""},
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
        )
        self.assertEqual(response.status_code, 400)

    def test_suggest_endpoint_with_learn(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.suggest_url, {"past_word": self.past_word2})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("suggestions", data)
        self.assertNotEqual(len(data["suggestions"]), 0)
        self.assertEqual(self.suggestion2 in data["suggestions"], False)

        response = self.client.post(
            self.learn_url,
            {"tokens": ["حافظ", "دروازه"], "username": self.user_data["username"]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            self.suggest_url,
            {"past_word": self.past_word2, "username": self.user_data["username"]},
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("suggestions", data)
        self.assertNotEqual(len(data["suggestions"]), 0)
        self.assertEqual(self.suggestion2 in data["suggestions"], True)
