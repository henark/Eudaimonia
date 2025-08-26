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

    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="core_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions",
        related_query_name="user",
    )
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class LivingWorld(models.Model):
    """
    LivingWorld model - a community for collaborative world-building.

    This model represents a "Living World," a community-driven space with its
    own unique theme, rules, and governance. It is the central pillar of the
    Eudaimonia platform, where users can create and join communities that
    align with their interests.
    """
    THEME_CHOICES = [
        ('decentralized_science', 'Decentralized Science'),
        ('art_and_culture', 'Art and Culture'),
        ('technology_and_startups', 'Technology and Startups'),
        ('social_and_political_issues', 'Social and Political Issues'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    theme = models.CharField(
        max_length=50,
        choices=THEME_CHOICES,
        default='other'
    )
    # The `theme_data` field allows for flexible, theme-specific data
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
    Post model - a piece of content within a LivingWorld.

    This model represents a single post made by a user within a LivingWorld.
    Posts are always contextual to a world, preventing the context collapse
    common in traditional social media feeds.
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
        return f"Post by {self.author.username} in {self.world.name}"


class ResearchArtifact(models.Model):
    """
    ResearchArtifact model - a piece of scientific work.
    """
    ARTIFACT_TYPES = [
        ('preprint', 'Pre-print'),
        ('dataset', 'Dataset'),
        ('code', 'Code'),
        ('review', 'Review'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    abstract = models.TextField()
    artifact_type = models.CharField(max_length=50, choices=ARTIFACT_TYPES)
    ipfs_cid = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artifacts'
    )
    world = models.ForeignKey(
        LivingWorld,
        on_delete=models.CASCADE,
        related_name='artifacts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'research_artifact'
        verbose_name = 'Research Artifact'
        verbose_name_plural = 'Research Artifacts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"


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
    CommunityMembership model - the bridge between Users and ResearchHubs.
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
        unique_together = ['user', 'hub']
    
    def __str__(self):
        return f"{self.user.username} in {self.hub.name} ({self.role})"


class PeerReview(models.Model):
    """
    PeerReview model for scientific artifacts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artifact = models.ForeignKey(
        ResearchArtifact,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'peer_review'
        verbose_name = 'Peer Review'
        verbose_name_plural = 'Peer Reviews'
        unique_together = ['artifact', 'reviewer']

    def __str__(self):
        return f"Review of {self.artifact.title} by {self.reviewer.username}"


class Citation(models.Model):
    """
    Citation model to track citations between artifacts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citing_artifact = models.ForeignKey(
        ResearchArtifact,
        on_delete=models.CASCADE,
        related_name='citations_made'
    )
    cited_artifact = models.ForeignKey(
        ResearchArtifact,
        on_delete=models.CASCADE,
        related_name='citations_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'citation'
        verbose_name = 'Citation'
        verbose_name_plural = 'Citations'
        unique_together = ['citing_artifact', 'cited_artifact']


class Proposal(models.Model):
    """
    Proposal model for community governance.
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