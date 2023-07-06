"""
Test models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model # Better to use custom get_user_model function.

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Testing that creating a new user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        # Check password is encrypted.
        self.assertTrue(user.check_password(password))
        