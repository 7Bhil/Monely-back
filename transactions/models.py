from django.db import models
from django.conf import settings


class Transaction(models.Model):
    """
    Transaction model for tracking income and expenses.
    """
    TYPE_CHOICES = [
        ('income', 'Revenu'),
        ('expense', 'Dépense'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Terminée'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Utilisateur"
    )
    wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Portefeuille"
    )
    receiver_wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transfers',
        verbose_name="Portefeuille destinataire"
    )
    name = models.CharField(max_length=255, verbose_name="Nom de la transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    type = models.CharField(
        max_length=10, 
        choices=TYPE_CHOICES + [('transfer', 'Transfert')], 
        verbose_name="Type"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed', verbose_name="Statut")
    date = models.DateTimeField(verbose_name="Date de la transaction")
    icon = models.CharField(max_length=50, default='attach_money', verbose_name="Icône")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['wallet', '-date']),
            models.Index(fields=['type', '-date']),
            models.Index(fields=['category', '-date']),
        ]
    
    def __str__(self):
        sign = '+' if self.type == 'income' else '-'
        if self.type == 'transfer':
            sign = '⇄'
        return f"{self.name} ({sign}{self.amount})"
    
    def save(self, *args, **kwargs):
        """Override save to update wallet balance"""
        is_new = self.pk is None
        old_amount = 0
        old_type = None
        old_wallet = None
        old_receiver_wallet = None
        
        if not is_new:
            old_transaction = Transaction.objects.get(pk=self.pk)
            old_amount = old_transaction.amount
            old_type = old_transaction.type
            old_wallet = old_transaction.wallet
            old_receiver_wallet = old_transaction.receiver_wallet
        
        super().save(*args, **kwargs)
        
        # Update wallet balance
        if is_new:
            if self.type == 'income':
                self.wallet.balance += self.amount
            elif self.type == 'expense':
                self.wallet.balance -= self.amount
            elif self.type == 'transfer' and self.receiver_wallet:
                self.wallet.balance -= self.amount
                self.receiver_wallet.balance += self.amount
                self.receiver_wallet.save()
        else:
            # Revert old balance changes
            if old_type == 'income':
                old_wallet.balance -= old_amount
            elif old_type == 'expense':
                old_wallet.balance += old_amount
            elif old_type == 'transfer' and old_receiver_wallet:
                old_wallet.balance += old_amount
                old_receiver_wallet.balance -= old_amount
                old_receiver_wallet.save()
            
            if old_wallet != self.wallet:
                old_wallet.save()
            
            # Apply new balance changes
            if self.type == 'income':
                self.wallet.balance += self.amount
            elif self.type == 'expense':
                self.wallet.balance -= self.amount
            elif self.type == 'transfer' and self.receiver_wallet:
                self.wallet.balance -= self.amount
                self.receiver_wallet.balance += self.amount
                self.receiver_wallet.save()
        
        self.wallet.save()
    
    def delete(self, *args, **kwargs):
        """Override delete to update wallet balance"""
        # Revert the balance change
        if self.type == 'income':
            self.wallet.balance -= self.amount
        else:
            self.wallet.balance += self.amount
        
        self.wallet.save()
        super().delete(*args, **kwargs)
