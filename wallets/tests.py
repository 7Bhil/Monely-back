from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from .models import Wallet


class WalletTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='wallettest@example.com',
            username='walletuser',
            name='Wallet User',
            password='StrongPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.wallet_url = '/api/wallets/wallets/'

    def test_create_wallet(self):
        """Test that a user can create a wallet."""
        data = {
            'name': 'Mon Compte',
            'type': 'checking',
            'balance': '500.00',
            'currency': 'EUR',
            'color': 'blue',
            'icon': 'account_balance',
        }
        response = self.client.post(self.wallet_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Wallet.objects.filter(name='Mon Compte', user=self.user).exists())

    def test_list_wallets_only_own(self):
        """Test that a user only sees their own wallets."""
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otherwallet',
            name='Other',
            password='StrongPass123!'
        )
        Wallet.objects.create(
            user=self.user, name='My Wallet', type='checking', balance=0, currency='EUR'
        )
        Wallet.objects.create(
            user=other_user, name='Their Wallet', type='savings', balance=0, currency='EUR'
        )
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        names = [w['name'] for w in results]
        self.assertIn('My Wallet', names)
        self.assertNotIn('Their Wallet', names)

    def test_wallet_requires_auth(self):
        """Test that unauthenticated requests are rejected."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
