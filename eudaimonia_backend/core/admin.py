from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (
    LivingWorld, Post, Friendship, CommunityMembership,
    Proposal, Vote, SmartProfile, VerifiableCredential, DataExport
)

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_active']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Eudaimonia Info', {'fields': ('preferred_ai_provider',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Eudaimonia Info', {'fields': ('preferred_ai_provider',)}),
    )

@admin.register(LivingWorld)
class LivingWorldAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'member_count', 'created_at']
    list_filter = ['created_at', 'category']
    search_fields = ['name', 'description', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Members'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'world', 'content_preview', 'created_at']
    list_filter = ['created_at', 'world']
    search_fields = ['content', 'author__username', 'world__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user1__username', 'user2__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(SmartProfile)
class SmartProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'did', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'did', 'user__username']
    readonly_fields = ['id', 'did', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(VerifiableCredential)
class VerifiableCredentialAdmin(admin.ModelAdmin):
    list_display = ['profile', 'issuer_did', 'issued_at']
    list_filter = ['issued_at', 'issuer_did']
    search_fields = ['profile__name', 'issuer_did']
    readonly_fields = ['id', 'issued_at']
    ordering = ['-issued_at']

@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ['profile', 'world', 'role', 'reputation', 'joined_at']
    list_filter = ['role', 'joined_at', 'world']
    search_fields = ['profile__name', 'world__name']
    readonly_fields = ['id', 'joined_at', 'updated_at']
    ordering = ['-joined_at']

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'world', 'vote_count', 'created_at']
    list_filter = ['created_at', 'world']
    search_fields = ['title', 'description', 'creator__username', 'world__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def vote_count(self, obj):
        return obj.votes.count()
    vote_count.short_description = 'Votes'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'proposal', 'choice', 'created_at']
    list_filter = ['choice', 'created_at', 'proposal__world']
    search_fields = ['voter__username', 'proposal__title']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

@admin.register(DataExport)
class DataExportAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ipfs_cid', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'ipfs_cid']
    readonly_fields = ['id', 'created_at', 'updated_at', 'ipfs_cid']
    ordering = ['-created_at']
