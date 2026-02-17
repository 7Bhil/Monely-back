from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TransactionSerializer, TransactionCreateSerializer
from .models import Transaction

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['wallet', 'type', 'category', 'status']
    ordering_fields = ['date', 'amount', 'created_at']
    search_fields = ['name', 'category']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransactionCreateSerializer
        return TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
