from rest_framework import serializers
from .models import Wallet, SavingGoal, FixedExpense


class WalletSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'id', 'name', 'type', 'type_display', 'balance', 
            'currency', 'color', 'icon', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')


class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('name', 'type', 'balance', 'currency', 'color', 'icon')


class SavingGoalSerializer(serializers.ModelSerializer):
    progress = serializers.FloatField(source='progress_percentage', read_only=True)
    
    class Meta:
        model = SavingGoal
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class SavingGoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = ('name', 'target_amount', 'current_amount', 'deadline', 'color')


class FixedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpense
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class FixedExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpense
        fields = ('name', 'amount', 'currency', 'periodicity', 'start_date')
