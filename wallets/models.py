from django.db import models
from django.conf import settings


class Wallet(models.Model):
    """
    Wallet/Account model representing different financial accounts.
    Can be checking account, savings, or credit card.
    """
    TYPE_CHOICES = [
        ('checking', 'Compte Courant'),
        ('savings', 'Compte Épargne'),
        ('credit', 'Carte de Crédit'),
        ('investment', 'Investissement'),
        ('cash', 'Espèces'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallets',
        verbose_name="Utilisateur"
    )
    name = models.CharField(max_length=150, verbose_name="Nom du compte")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de compte")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Solde")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Devise")
    color = models.CharField(max_length=50, default='blue', verbose_name="Couleur")
    icon = models.CharField(max_length=50, default='account_balance', verbose_name="Icône")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Portefeuille"
        verbose_name_plural = "Portefeuilles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class SavingGoal(models.Model):
    """
    Saving Goal model for tracking user's financial objectives.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saving_goals',
        verbose_name="Utilisateur"
    )
    name = models.CharField(max_length=150, verbose_name="Nom de l'objectif")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant cible")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant actuel")
    deadline = models.DateField(verbose_name="Date limite")
    color = models.CharField(max_length=50, default='blue', verbose_name="Couleur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Objectif d'épargne"
        verbose_name_plural = "Objectifs d'épargne"
        ordering = ['deadline']
        indexes = [
            models.Index(fields=['user', 'deadline']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.current_amount}/{self.target_amount}"
    
    @property
    def progress_percentage(self):
        """Calculate the progress percentage"""
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0


class FixedExpense(models.Model):
    """
    Model for recurring fixed expenses (Rent, Netflix, Insurance, etc.)
    """
    PERIODICITY_CHOICES = [
        ('monthly', 'Mensuel'),
        ('weekly', 'Hebdomadaire'),
        ('yearly', 'Annuel'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fixed_expenses',
        verbose_name="Utilisateur"
    )
    name = models.CharField(max_length=150, verbose_name="Nom de la charge")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Devise")
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, default='monthly', verbose_name="Périodicité")
    start_date = models.DateField(verbose_name="Date de début", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "Charge fixe"
        verbose_name_plural = "Charges fixes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"
