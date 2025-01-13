from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


class UserSignupTestCase(TestCase):
    def test_signup_user(self):
        """Test that a user can sign up successfully."""
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'name': 'Test User',
            'age': 25,
        }
        response = self.client.post(reverse('group9:signup'), data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful sign-up
        self.assertTrue(User.objects.filter(username='testuser').exists())
        