"""
Main API URLs for Eudaimonia Core App

This module provides URL patterns for all API endpoints,
including ViewSets for models and custom endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LivingWorldViewSet, PostViewSet, FriendshipViewSet,
    CommunityMembershipViewSet, ProposalViewSet, VoteViewSet, AICompanionView,
    SmartProfileViewSet, VerifiableCredentialViewSet, DataExportViewSet
)

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'worlds', LivingWorldViewSet)
router.register(r'posts', PostViewSet)
router.register(r'friendships', FriendshipViewSet)
router.register(r'memberships', CommunityMembershipViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'profiles', SmartProfileViewSet, basename='smartprofile')
router.register(r'credentials', VerifiableCredentialViewSet, basename='verifiablecredential')
router.register(r'exports', DataExportViewSet, basename='dataexport')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('companion/query/', AICompanionView.as_view(), name='ai-companion'),
] 