"""
Eudaimonia Core Views

This module provides Django REST Framework views and ViewSets for all models,
implementing the API endpoints that power the Eudaimonia platform. The views
are designed to support the community-centric architecture and implement
the faceted identity concepts outlined in the project principles.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import (
    LivingWorld, Post, Friendship, CommunityMembership,
    Proposal, Vote
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LivingWorldSerializer,
    PostSerializer, FriendshipSerializer, CommunityMembershipSerializer,
    ProposalSerializer, VoteSerializer, FacetedProfileSerializer
)

User = get_user_model()


class UserRegistrationView(APIView):
    """
    User registration endpoint.
    
    This view handles user registration with proper validation
    and password hashing.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User ViewSet for user management.
    
    This ViewSet provides read-only access to user information,
    maintaining security by not exposing sensitive data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Get a user's faceted profile.
        
        This endpoint materializes the "Faceted Identity" concept by
        returning a user's identity as the intersection of their
        community affiliations.
        """
        user = self.get_object()
        serializer = FacetedProfileSerializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def friends(self, request, pk=None):
        """
        Get a user's friends list.
        
        This endpoint returns all accepted friendships for a user.
        """
        user = self.get_object()
        friendships = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user),
            status='accepted'
        )
        
        friends = []
        for friendship in friendships:
            if friendship.user1 == user:
                friends.append(UserSerializer(friendship.user2).data)
            else:
                friends.append(UserSerializer(friendship.user1).data)
        
        return Response(friends)


class LivingWorldViewSet(viewsets.ModelViewSet):
    """
    LivingWorld ViewSet for community management.
    
    This ViewSet provides full CRUD operations for LivingWorlds,
    with the owner being automatically set to the current user.
    """
    queryset = LivingWorld.objects.all()
    serializer_class = LivingWorldSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """
        Join a LivingWorld.
        
        This endpoint allows users to join a LivingWorld, creating
        a CommunityMembership with default role and reputation.
        """
        world = self.get_object()
        serializer = CommunityMembershipSerializer(
            data={'world_id': world.id},
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """
        Get all posts in a LivingWorld.
        
        This endpoint returns all posts within a specific LivingWorld,
        maintaining the contextual nature of content.
        """
        world = self.get_object()
        posts = world.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """
        Get all members of a LivingWorld.
        
        This endpoint returns all CommunityMemberships for a LivingWorld,
        showing the community structure.
        """
        world = self.get_object()
        memberships = world.memberships.all()
        serializer = CommunityMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    Post ViewSet for content management.
    
    This ViewSet provides full CRUD operations for posts within
    LivingWorlds, ensuring content is always contextual.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter posts by LivingWorld if world_id is provided.
        """
        queryset = Post.objects.all()
        world_id = self.request.query_params.get('world_id', None)
        if world_id:
            queryset = queryset.filter(world_id=world_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FriendshipViewSet(viewsets.ModelViewSet):
    """
    Friendship ViewSet for relationship management.
    
    This ViewSet handles friendship requests and management,
    implementing the social graph aspect of Eudaimonia.
    """
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter friendships to show only those involving the current user.
        """
        return Friendship.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Accept a friendship request.
        """
        friendship = self.get_object()
        if friendship.user2 == request.user and friendship.status == 'pending':
            friendship.status = 'accepted'
            friendship.save()
            return Response({'status': 'accepted'})
        return Response(
            {'error': 'Cannot accept this friendship request'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a friendship request.
        """
        friendship = self.get_object()
        if friendship.user2 == request.user and friendship.status == 'pending':
            friendship.status = 'rejected'
            friendship.save()
            return Response({'status': 'rejected'})
        return Response(
            {'error': 'Cannot reject this friendship request'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get pending friendship requests.
        """
        pending_friendships = Friendship.objects.filter(
            user2=request.user,
            status='pending'
        )
        serializer = self.get_serializer(pending_friendships, many=True)
        return Response(serializer.data)


class CommunityMembershipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    CommunityMembership ViewSet for membership management.
    
    This ViewSet provides read-only access to CommunityMemberships,
    with creation handled through the LivingWorld join endpoint.
    """
    queryset = CommunityMembership.objects.all()
    serializer_class = CommunityMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter memberships to show only those of the current user.
        """
        return CommunityMembership.objects.filter(user=self.request.user)


class ProposalViewSet(viewsets.ModelViewSet):
    """
    Proposal ViewSet for governance management.
    
    This ViewSet provides full CRUD operations for governance
    proposals within LivingWorlds.
    """
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter proposals by LivingWorld if world_id is provided.
        """
        queryset = Proposal.objects.all()
        world_id = self.request.query_params.get('world_id', None)
        if world_id:
            queryset = queryset.filter(world_id=world_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['get'])
    def votes(self, request, pk=None):
        """
        Get all votes for a proposal.
        """
        proposal = self.get_object()
        votes = proposal.votes.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)


class VoteViewSet(viewsets.ModelViewSet):
    """
    Vote ViewSet for voting management.
    
    This ViewSet handles voting on governance proposals,
    implementing the basic governance mechanism.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter votes to show only those of the current user.
        """
        return Vote.objects.filter(voter=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)


class SocialRecoveryView(APIView):
    """
    Social Recovery endpoint (placeholder for future implementation).
    
    This endpoint serves as a roadmap marker for the future
    implementation of social recovery using ERC-4337 Account Abstraction.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Placeholder for social recovery functionality.
        
        In the future, this will implement social recovery using
        ERC-4337 Account Abstraction, allowing users to recover
        their accounts through their social graph.
        """
        return Response(
            {
                'message': 'Social recovery feature planned for future decentralized version',
                'planned_implementation': 'ERC-4337 Account Abstraction for social recovery'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class AICompanionView(APIView):
    """
    AI Companion endpoint for contextual AI assistance.
    
    This endpoint provides personalized AI assistance based on
    the user's faceted identity and community context.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Process AI companion queries with user context.
        
        This endpoint takes a user query and enriches it with
        the user's faceted profile data before sending to an
        external LLM API for personalized responses.
        """
        query = request.data.get('query', '')
        if not query:
            return Response(
                {'error': 'Query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user's faceted profile
        user = request.user
        profile_serializer = FacetedProfileSerializer(user)
        user_context = profile_serializer.data
        
        # Construct meta-prompt with user context
        system_message = (
            "You are an AI companion helping a user navigate their social world "
            "on Eudaimonia. You understand the concept of 'Faceted Identity' "
            "where a person's identity emerges from their various community "
            "affiliations and roles."
        )
        
        context_message = f"User context: {user_context}"
        full_prompt = f"{system_message}\n\n{context_message}\n\nUser question: {query}"
        
        # TODO: Integrate with OpenAI API
        # For now, return a placeholder response
        response = {
            'message': 'AI Companion feature is being implemented',
            'user_context': user_context,
            'query': query,
            'planned_integration': 'OpenAI API for personalized responses'
        }
        
        return Response(response) 