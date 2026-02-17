from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'wallet', 'wallet_name', 'name', 'amount', 'category',
            'type', 'type_display', 'status', 'status_display',
            'date', 'icon', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_amount(self, value):
        """Ensure amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être positif.")
        return value


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions"""
    
    class Meta:
        model = Transaction
        fields = ('wallet', 'name', 'amount', 'category', 'type', 'status', 'date', 'icon')
