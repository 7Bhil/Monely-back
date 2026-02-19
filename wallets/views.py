from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wallet, SavingGoal, FixedExpense
from .serializers import (
    WalletSerializer, WalletCreateSerializer,
    SavingGoalSerializer, SavingGoalCreateSerializer,
    FixedExpenseSerializer, FixedExpenseCreateSerializer
)


class WalletViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WalletCreateSerializer
        return WalletSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"--- WALLET VALIDATION ERROR ---")
            print(f"Payload: {request.data}")
            print(f"Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingGoalViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SavingGoalCreateSerializer
        return SavingGoalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FixedExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['periodicity', 'currency']
    ordering_fields = ['amount', 'start_date', 'created_at']
    search_fields = ['name']
    
    def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FixedExpenseCreateSerializer
        return FixedExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
