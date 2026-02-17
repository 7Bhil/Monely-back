from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for Monely.
    Extends Django's AbstractUser with additional fields for financial management.
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=150, verbose_name="Nom complet")
    avatar_url = models.URLField(blank=True, null=True, verbose_name="URL de l'avatar")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Devise")
    language = models.CharField(max_length=5, default='fr', verbose_name="Langue")
    
    # Financial Profile
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Revenu mensuel")
    INCOME_FREQUENCY_CHOICES = [
        ('monthly', 'Mensuel'),
        ('weekly', 'Hebdomadaire'),
        ('yearly', 'Annuel'),
    ]
    income_frequency = models.CharField(max_length=20, choices=INCOME_FREQUENCY_CHOICES, default='monthly', verbose_name="Fréquence du revenu")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    # Override username to use email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
