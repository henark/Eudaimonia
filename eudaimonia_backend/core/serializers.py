"""
Eudaimonia Core Serializers

This module provides Django REST Framework serializers for all models,
enabling the API endpoints that power the Eudaimonia platform. The serializers
are designed to reflect the community-centric architecture and faceted identity
concepts outlined in the project principles.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    LivingWorld, Post, Friendship, CommunityMembership,
    Proposal, Vote
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for basic user information.
    
    This serializer provides a clean interface for user data while
    maintaining security by excluding sensitive fields.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer with password validation.
    
    This serializer handles user registration with proper password
    hashing and validation.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LivingWorldSerializer(serializers.ModelSerializer):
    """
    LivingWorld serializer for community data.
    
    This serializer includes the owner information and provides
    a complete view of a LivingWorld's structure and theme.
    """
    owner = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LivingWorld
        fields = [
            'id', 'name', 'description', 'theme_data',
            'owner', 'created_at', 'member_count'
        ]
        read_only_fields = ['id', 'owner', 'created_at']
    
    def get_member_count(self, obj):
        return obj.memberships.count()


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer for content within LivingWorlds.
    
    This serializer includes author information and ensures posts
    are always contextual to their LivingWorld.
    """
    author = UserSerializer(read_only=True)
    world = LivingWorldSerializer(read_only=True)
    world_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'content', 'author', 'world', 'world_id',
            'created_at'
        ]
        read_only_fields = ['id', 'author', 'created_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['world'] = LivingWorld.objects.get(
            id=validated_data.pop('world_id')
        )
        return super().create(validated_data)


class FriendshipSerializer(serializers.ModelSerializer):
    """
    Friendship serializer for user relationships.
    
    This serializer handles the creation and management of
    friendship relationships between users.
    """
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    user2_username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Friendship
        fields = [
            'id', 'user1', 'user2', 'user2_username',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'user1', 'status', 'created_at']
    
    def create(self, validated_data):
        user2_username = validated_data.pop('user2_username')
        try:
            user2 = User.objects.get(username=user2_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        validated_data['user1'] = self.context['request'].user
        validated_data['user2'] = user2
        
        # Check if friendship already exists
        if Friendship.objects.filter(
            user1=validated_data['user1'],
            user2=validated_data['user2']
        ).exists():
            raise serializers.ValidationError("Friendship request already exists")
        
        return super().create(validated_data)


class CommunityMembershipSerializer(serializers.ModelSerializer):
    """
    CommunityMembership serializer for user-world relationships.

    This serializer implements the "Faceted Identity" concept by
    showing a user's role and reputation within a specific LivingWorld.
    """
    user = UserSerializer(read_only=True)
    world = LivingWorldSerializer(read_only=True)
    world_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CommunityMembership
        fields = [
            'id', 'user', 'world', 'world_id', 'role',
            'reputation', 'joined_at'
        ]
        read_only_fields = ['id', 'user', 'role', 'reputation', 'joined_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['world'] = LivingWorld.objects.get(
            id=validated_data.pop('world_id')
        )

        # Check if membership already exists
        if CommunityMembership.objects.filter(
            user=validated_data['user'],
            world=validated_data['world']
        ).exists():
            raise serializers.ValidationError("Already a member of this world")

        return super().create(validated_data)


class ProposalSerializer(serializers.ModelSerializer):
    """
    Proposal serializer for community governance.
    
    This serializer handles the creation and display of governance
    proposals within LivingWorlds.
    """
    creator = UserSerializer(read_only=True)
    world = LivingWorldSerializer(read_only=True)
    world_id = serializers.UUIDField(write_only=True)
    vote_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Proposal
        fields = [
            'id', 'title', 'description', 'creator', 'world',
            'world_id', 'created_at', 'vote_count'
        ]
        read_only_fields = ['id', 'creator', 'created_at']
    
    def get_vote_count(self, obj):
        return obj.votes.count()
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['world'] = LivingWorld.objects.get(
            id=validated_data.pop('world_id')
        )
        return super().create(validated_data)


class VoteSerializer(serializers.ModelSerializer):
    """
    Vote serializer for proposal voting.
    
    This serializer handles the voting mechanism for governance
    proposals within LivingWorlds.
    """
    voter = UserSerializer(read_only=True)
    proposal = ProposalSerializer(read_only=True)
    proposal_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Vote
        fields = [
            'id', 'voter', 'proposal', 'proposal_id',
            'choice', 'created_at'
        ]
        read_only_fields = ['id', 'voter', 'created_at']
    
    def create(self, validated_data):
        validated_data['voter'] = self.context['request'].user
        validated_data['proposal'] = Proposal.objects.get(
            id=validated_data.pop('proposal_id')
        )
        
        # Check if user has already voted
        if Vote.objects.filter(
            voter=validated_data['voter'],
            proposal=validated_data['proposal']
        ).exists():
            raise serializers.ValidationError("Already voted on this proposal")
        
        return super().create(validated_data)


class FacetedProfileSerializer(serializers.ModelSerializer):
    """
    Faceted Profile serializer - the core of Eudaimonia's identity system.
    
    This serializer materializes the "Faceted Identity" concept by showing
    a user's identity as the intersection of their community affiliations.
    It returns basic user information along with their memberships across
    different LivingWorlds, including roles and reputations.
    """
    community_memberships = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'community_memberships']
        read_only_fields = ['id', 'date_joined']

    def get_community_memberships(self, obj):
        memberships = obj.community_memberships.select_related('world').all()
        return [
            {
                'world_name': membership.world.name,
                'world_description': membership.world.description,
                'role': membership.role,
                'reputation': membership.reputation,
                'joined_at': membership.joined_at
            }
            for membership in memberships
        ]