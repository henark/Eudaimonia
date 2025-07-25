"""
Eudaimonia Core Models

This module implements the database schema based on the Eudaimonia Principles.
The architecture prioritizes LivingWorlds (communities) as the primary entities,
with users and content contextually situated within them, reflecting the
philosophy of "Faceted Identity" and community-centric design.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Extended User model for Eudaimonia.
    
    This model represents individual users in the system. Following the
    "Faceted Identity" principle, a user's identity is not monolithic but
    emerges from their various roles and relationships across different
    "Living Worlds."
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    
    # Override username to ensure uniqueness
    username = models.CharField(max_length=150, unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class LivingWorld(models.Model):
    """
    LivingWorld model - the central entity in Eudaimonia's architecture.
    
    A LivingWorld represents a distinct community space where users can
    interact, share content, and build relationships. Each world has its
    own theme, rules, and culture, embodying the concept of contextual
    social spaces.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    theme_data = models.JSONField(default=dict, blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_worlds'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'living_world'
        verbose_name = 'Living World'
        verbose_name_plural = 'Living Worlds'
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Post model for content within LivingWorlds.
    
    Posts are always contextual to a specific LivingWorld, reinforcing
    the community-centric architecture. This prevents context collapse
    by ensuring content is always situated within its appropriate social
    context.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    world = models.ForeignKey(
        LivingWorld, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} in {self.world.name}: {self.content[:50]}..."


class Friendship(models.Model):
    """
    Friendship model for user relationships.
    
    This implements the social graph aspect of Eudaimonia, allowing users
    to form direct connections while maintaining their contextual identities
    within different LivingWorlds.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friendships_initiated'
    )
    user2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friendships_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'friendship'
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'
        unique_together = ['user1', 'user2']
    
    def __str__(self):
        return f"{self.user1.username} - {self.user2.username} ({self.status})"


class CommunityMembership(models.Model):
    """
    CommunityMembership model - the bridge between Users and LivingWorlds.
    
    This model implements the "Faceted Identity" concept by tracking a user's
    role, reputation, and participation within each LivingWorld they join.
    A user's identity emerges from the intersection of these various memberships.
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='community_memberships'
    )
    world = models.ForeignKey(
        LivingWorld, 
        on_delete=models.CASCADE, 
        related_name='memberships'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    reputation = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'community_membership'
        verbose_name = 'Community Membership'
        verbose_name_plural = 'Community Memberships'
        unique_together = ['user', 'world']
    
    def __str__(self):
        return f"{self.user.username} in {self.world.name} ({self.role})"


class Proposal(models.Model):
    """
    Proposal model for community governance.
    
    This implements the basic governance system for LivingWorlds, allowing
    communities to make collective decisions. This is the foundation for
    the future DAO functionality outlined in the roadmap.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    world = models.ForeignKey(
        LivingWorld, 
        on_delete=models.CASCADE, 
        related_name='proposals'
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='proposals_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proposal'
        verbose_name = 'Proposal'
        verbose_name_plural = 'Proposals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} in {self.world.name}"


class Vote(models.Model):
    """
    Vote model for proposal voting.
    
    This tracks individual votes on proposals, implementing the basic
    governance mechanism. In the future, this will be enhanced with
    more sophisticated voting mechanisms and on-chain execution.
    """
    CHOICE_CHOICES = [
        ('agree', 'Agree'),
        ('disagree', 'Disagree'),
        ('abstain', 'Abstain'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey(
        Proposal, 
        on_delete=models.CASCADE, 
        related_name='votes'
    )
    voter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='votes_cast'
    )
    choice = models.CharField(max_length=10, choices=CHOICE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ['proposal', 'voter']
    
    def __str__(self):
        return f"{self.voter.username} voted {self.choice} on {self.proposal.title}" 