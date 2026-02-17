from django.contrib import admin
from .models import Wallet, SavingGoal


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Admin configuration for Wallet model"""
    list_display = ('name', 'type', 'user', 'balance', 'currency', 'created_at')
    list_filter = ('type', 'currency', 'created_at')
    search_fields = ('name', 'user__email', 'user__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'name', 'type')
        }),
        ('Finances', {
            'fields': ('balance', 'currency')
        }),
        ('Apparence', {
            'fields': ('color', 'icon')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    """Admin configuration for SavingGoal model"""
    list_display = ('name', 'user', 'current_amount', 'target_amount', 'progress_percentage', 'deadline')
    list_filter = ('deadline', 'created_at')
    search_fields = ('name', 'user__email', 'user__name')
    ordering = ('deadline',)
    readonly_fields = ('created_at', 'updated_at', 'progress_percentage')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'name', 'color')
        }),
        ('Objectif', {
            'fields': ('target_amount', 'current_amount', 'deadline')
        }),
        ('Progression', {
            'fields': ('progress_percentage',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
