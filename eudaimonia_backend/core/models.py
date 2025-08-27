import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    preferred_ai_provider = models.CharField(max_length=50, default='openai')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    WORLD_CATEGORIES = [
        ('education', 'Education'),
        ('art', 'Art'),
        ('science', 'Science'),
        ('social_participation', 'Social Participation'),
        ('hobbies', 'Hobbies'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(
        max_length=50, 
        choices=WORLD_CATEGORIES, 
        default='other'
    )
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


class SmartProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='smart_profiles'
    )
    name = models.CharField(max_length=100)
    did = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'smart_profile'
        verbose_name = 'Smart Profile'
        verbose_name_plural = 'Smart Profiles'
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.user.username}'s {self.name} Profile"


class VerifiableCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        SmartProfile,
        on_delete=models.CASCADE,
        related_name='credentials'
    )
    credential_data = models.JSONField()
    issuer_did = models.CharField(max_length=255)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'verifiable_credential'
        verbose_name = 'Verifiable Credential'
        verbose_name_plural = 'Verifiable Credentials'

    def __str__(self):
        return f"VC for {self.profile.name} issued by {self.issuer_did}"


class CommunityMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        SmartProfile,
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
        unique_together = ['profile', 'world']
    
    def __str__(self):
        return f"{self.profile.name} in {self.world.name} ({self.role})"


class Proposal(models.Model):
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


class DataExport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_exports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ipfs_cid = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_export'
        verbose_name = 'Data Export'
        verbose_name_plural = 'Data Exports'

    def __str__(self):
        return f"Export for {self.user.username} at {self.created_at}"
