"""
Eudaimonia Core ViewSets

This module provides Django REST Framework ViewSets for the SmartProfile
and VerifiableCredential models.
"""

from rest_framework import viewsets, permissions
from .models import SmartProfile, VerifiableCredential
from .serializers import SmartProfileSerializer, VerifiableCredentialSerializer


class SmartProfileViewSet(viewsets.ModelViewSet):
    """
    SmartProfile ViewSet for managing faceted identities.
    """
    queryset = SmartProfile.objects.all()
    serializer_class = SmartProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter SmartProfiles to show only those of the current user.
        """
        return SmartProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the user of the SmartProfile to the current user.
        """
        serializer.save(user=self.request.user)


class VerifiableCredentialViewSet(viewsets.ModelViewSet):
    """
    VerifiableCredential ViewSet for managing credentials.
    """
    queryset = VerifiableCredential.objects.all()
    serializer_class = VerifiableCredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter VerifiableCredentials to show only those of the current user's
        SmartProfiles.
        """
        return VerifiableCredential.objects.filter(profile__user=self.request.user)
