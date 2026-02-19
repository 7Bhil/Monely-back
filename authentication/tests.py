from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.profile_url = '/api/auth/profile/'

    def test_register_user(self):
        """Test that a new user can register successfully."""
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'username': 'testuser',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_password_mismatch(self):
        """Test that mismatched passwords are rejected."""
        data = {
            'email': 'test2@example.com',
            'name': 'Test User',
            'username': 'testuser2',
            'password': 'StrongPass123!',
            'password_confirm': 'WrongPass!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Test that a registered user can log in and receive tokens."""
        User.objects.create_user(
            email='login@example.com',
            username='loginuser',
            name='Login User',
            password='StrongPass123!'
        )
        data = {'email': 'login@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_requires_auth(self):
        """Test that the profile endpoint requires authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        """Test that an authenticated user can fetch their profile."""
        user = User.objects.create_user(
            email='profile@example.com',
            username='profileuser',
            name='Profile User',
            password='StrongPass123!'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'profile@example.com')
