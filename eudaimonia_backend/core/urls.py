"""
Authentication URLs for Eudaimonia Core App

This module provides URL patterns for authentication endpoints,
including user registration and social recovery.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, SocialRecoveryView, MeView, MyProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('recovery/initiate/', SocialRecoveryView.as_view(), name='social-recovery'),
    path('me/', MeView.as_view(), name='me'),
    path('me/profile/', MyProfileView.as_view(), name='me-profile'),
] 