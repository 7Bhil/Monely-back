from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    list_display = ('email', 'name', 'currency', 'language', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'currency', 'language')
    search_fields = ('email', 'name', 'username')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Monely', {'fields': ('avatar_url', 'currency', 'language')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations Monely', {'fields': ('email', 'name', 'avatar_url', 'currency', 'language')}),
    )
