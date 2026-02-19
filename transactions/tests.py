from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from wallets.models import Wallet
from .models import Transaction


class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='txtest@example.com',
            username='txuser',
            name='TX User',
            password='StrongPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.wallet = Wallet.objects.create(
            user=self.user,
            name='Compte Principal',
            type='checking',
            balance=1000,
            currency='EUR'
        )
        self.tx_url = '/api/transactions/transactions/'

    def test_create_income_updates_balance(self):
        """Creating an income transaction should increase wallet balance."""
        data = {
            'wallet': self.wallet.id,
            'name': 'Salaire',
            'amount': '500.00',
            'type': 'income',
            'category': 'Revenu',
            'date': '2026-02-01T10:00:00Z',
            'status': 'completed',
        }
        response = self.client.post(self.tx_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 1500.0)

    def test_create_expense_updates_balance(self):
        """Creating an expense transaction should decrease wallet balance."""
        data = {
            'wallet': self.wallet.id,
            'name': 'Courses',
            'amount': '200.00',
            'type': 'expense',
            'category': 'Nourriture',
            'date': '2026-02-01T10:00:00Z',
            'status': 'completed',
        }
        response = self.client.post(self.tx_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 800.0)

    def test_negative_amount_rejected(self):
        """A negative or zero amount should be rejected."""
        data = {
            'wallet': self.wallet.id,
            'name': 'Invalid',
            'amount': '-50.00',
            'type': 'expense',
            'category': 'Autre',
            'date': '2026-02-01T10:00:00Z',
            'status': 'completed',
        }
        response = self.client.post(self.tx_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_income_reverts_balance(self):
        """Deleting an income transaction should decrease wallet balance back."""
        tx = Transaction.objects.create(
            user=self.user,
            wallet=self.wallet,
            name='Salaire',
            amount=300,
            type='income',
            category='Revenu',
            date='2026-02-01T10:00:00Z',
            status='completed',
        )
        self.wallet.refresh_from_db()
        balance_after_create = float(self.wallet.balance)

        response = self.client.delete(f'{self.tx_url}{tx.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), balance_after_create - 300)

    def test_user_cannot_see_other_users_transactions(self):
        """A user should only see their own transactions."""
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            name='Other',
            password='StrongPass123!'
        )
        other_wallet = Wallet.objects.create(
            user=other_user, name='Other Wallet', type='checking', balance=0, currency='EUR'
        )
        Transaction.objects.create(
            user=other_user, wallet=other_wallet, name='Secret', amount=100,
            type='income', category='Revenu', date='2026-02-01T10:00:00Z', status='completed'
        )
        response = self.client.get(self.tx_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        for tx in results:
            self.assertNotEqual(tx['name'], 'Secret')
