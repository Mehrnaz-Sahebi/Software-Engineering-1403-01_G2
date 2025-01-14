from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from group9.logic import optimize_text, fetch_user_history
from django.test import TestCase
from unittest.mock import MagicMock

# Create your tests here.


class UserSignupTestCase(TestCase):
    def test_signup_user(self):
        """Test that a user can sign up successfully."""
        data = {
            "username": "user_group9",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password123",
            "name": "Test User",
            "age": 25,
        }
        response = self.client.post(reverse("group9:signup"), data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirects after successful sign-up
        self.assertTrue(User.objects.filter(username="user_group9").exists())

    def test_signup_password_mismatch(self):
        """Test that user gets an error when passwords do not match."""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password456",  # Password mismatch
            "name": "Test User",
            "age": 25,
        }
        response = self.client.post(reverse("group9:signup"), data)
        self.assertContains(
            response, "Your password and confirm password are not the same!"
        )


class UserLoginTestCase(TestCase):
    def setUp(self):
        """Create a user for login tests."""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_login_valid_user(self):
        """Test that a user can log in successfully."""
        response = self.client.post(
            reverse("group9:login"), {"username": "testuser", "pass": "password123"}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirects to the optimization page

    def test_login_invalid_user(self):
        """Test that an invalid user cannot log in."""
        response = self.client.post(
            reverse("group9:login"), {"username": "testuser", "pass": "wrongpassword"}
        )
        self.assertContains(response, "Username or Password is incorrect!!!")


class TextOptimizationTestCase(TestCase):
    def setUp(self):
        """Create a user and mock database connection for text optimization tests."""
        self.user = User.objects.create_user(
            username="userToCheckOptimization", password="password123"
        )
        self.mock_db_connection = MagicMock()  # Mock database connection

    def test_correct_spacing(self):
        """Test correcting extra spaces in the text."""
        input_text = "سلام   من     هستم"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=True,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "سلام من هستم")

    def test_remove_diacritics(self):
        """Test removing diacritical marks."""
        input_text = "عَلَيكُم"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=True,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "عليكم")

    def test_remove_special_characters(self):
        """Test removing special characters."""
        input_text = "پیامبر اکرم ﷺ"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=True,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "پیامبر اکرم ")

    def test_decrease_repeated_chars(self):
        """Test decreasing repeated characters."""
        input_text = "عاااالیییییی"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=True,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "عالی")

    def test_persian_style_formatting(self):
        """Test applying Persian style rules (e.g., replacing 'ي' with 'ی')."""
        input_text = "نرمال‌سازی 10.450"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=True,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "نرمال‌سازی 10٫450")

    def test_convert_to_persian_numbers(self):
        """Test converting numbers to Persian digits."""
        input_text = "1234567890"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=True,
            unicodes_replacement=False,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "۱۲۳۴۵۶۷۸۹۰")

    def test_unicode_replacement(self):
        """Test replacing specific Unicode characters."""
        input_text = "ﷴ"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=True,
            seperate_mi=False,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "محمد")

    def test_separate_mi(self):
        """Test separating 'می' from the next word."""
        input_text = "نمیدانم چه میگفت"
        optimized_text = optimize_text(
            input=input_text,
            user=self.user,
            correct_spacing=False,
            remove_diacrities=False,
            remove_special_chars=False,
            decrease_repeated_chars=False,
            persian_style=False,
            persian_number=False,
            unicodes_replacement=False,
            seperate_mi=True,
            db_connection=self.mock_db_connection,
        )
        self.assertEqual(optimized_text, "نمی‌دانم چه می‌گفت")


class UserHistoryTestCase(TestCase):
    def setUp(self):
        """Create a user and mock the database connection."""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.mock_db_connection = MagicMock()  # Mock database connection
        # Mock the return value of `get_user_history`
        self.mock_db_connection.cursor.return_value.fetchall.return_value = [
            (
                "input_text_example",
                "remove_special_chars",
                "Special characters removed",
                "correct form example",
                "2025-01-13",
            )
        ]

    def test_fetch_user_history(self):
        """Test fetching user history."""
        user_history = fetch_user_history(self.user.username, self.mock_db_connection)

        # Check the data is returned correctly
        self.assertEqual(len(user_history), 1)
        self.assertEqual(user_history[0]["type"], "remove_special_chars")
        self.assertEqual(user_history[0]["details"], "Special characters removed")
        self.assertEqual(user_history[0]["correct_form"], "correct form example")
        self.assertEqual(user_history[0]["Date"], "2025-01-13")
