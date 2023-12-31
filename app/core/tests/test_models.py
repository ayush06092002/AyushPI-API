"""Test for models"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

class ModelTests(TestCase):
    """Test Models."""


    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""

        # Creating a new user with an email.
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""

        # Creating a new user with an email.
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """"Test creating user without email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser) # is_superuser is included in PermissionsMixin
        self.assertTrue(user.is_staff)

    def test_create_medicine(self):
        """Test creating a new medicine"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        medicine = models.Medicine.objects.create(
            user = user,
            name = 'Sample Medicine',
            ref_text = 'Sample Reference Text',
            dispensing_size = 'Sample Dispensing Size',
            dosage = 'Sample Dosage',
            precautions = 'Sample Precautions',
            preferred_use = 'Sample Preferred Use',
        )

        self.assertEqual(str(medicine), medicine.name)

    def test_create_symptoms(self):
        """Test creating a new symptom"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        symptom = models.Symptom.objects.create(
            user = user,
            name = 'Sample Symptom',
        )

        self.assertEqual(str(symptom), symptom.name)




