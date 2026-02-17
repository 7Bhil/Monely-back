from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model"""
    list_display = ('name', 'type', 'amount', 'category', 'wallet', 'user', 'status', 'date')
    list_filter = ('type', 'status', 'category', 'date', 'created_at')
    search_fields = ('name', 'user__email', 'user__name', 'category')
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'wallet', 'name', 'type', 'status')
        }),
        ('Détails financiers', {
            'fields': ('amount', 'category', 'icon')
        }),
        ('Dates', {
            'fields': ('date',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'wallet')
