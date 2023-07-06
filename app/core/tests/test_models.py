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
        
    def test_new_user_email_normalized(self):
        """
        Testing that the email for a new user is normalized.
        """
        
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            
            # Note that we take the user.email, which
            # will be normalized upon creation.
            self.assertEqual(user.email, expected)    
    
    def test_new_user_without_email_raises_error(self):
        """Testing that creating a new user without an email will raise an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='test123')
            
    
    def test_create_super_user(self):
        """Test creating a user user."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        