from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, SavingGoalViewSet, FixedExpenseViewSet

router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'goals', SavingGoalViewSet, basename='saving-goal')
router.register(r'fixed-expenses', FixedExpenseViewSet, basename='fixed-expense')

urlpatterns = [
    path('', include(router.urls)),
]
