"""
Django Admin Configuration for Eudaimonia Core App

This module provides admin interface configurations for all models,
enabling administrative management of the Eudaimonia platform.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (
    LivingWorld, Post, Friendship, CommunityMembership,
    Proposal, Vote
)

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User admin interface.
    
    Extends the default UserAdmin to include custom fields
    and maintain the standard Django user management interface.
    """
    list_display = ['username', 'email', 'date_joined', 'is_active']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Eudaimonia Info', {'fields': ()}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Eudaimonia Info', {'fields': ()}),
    )


@admin.register(LivingWorld)
class LivingWorldAdmin(admin.ModelAdmin):
    """
    LivingWorld admin interface.
    
    Provides comprehensive management of LivingWorlds,
    including member counts and theme data.
    """
    list_display = ['name', 'owner', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Members'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin interface.
    
    Manages content posts within LivingWorlds,
    showing contextual relationships.
    """
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
    """
    Friendship admin interface.
    
    Manages user relationships and friendship requests.
    """
    list_display = ['user1', 'user2', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user1__username', 'user2__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    """
    CommunityMembership admin interface.
    
    Manages user-world relationships and roles.
    """
    list_display = ['user', 'world', 'role', 'reputation', 'joined_at']
    list_filter = ['role', 'joined_at', 'world']
    search_fields = ['user__username', 'world__name']
    readonly_fields = ['id', 'joined_at', 'updated_at']
    ordering = ['-joined_at']


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    """
    Proposal admin interface.
    
    Manages governance proposals within LivingWorlds.
    """
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
    """
    Vote admin interface.
    
    Manages voting on governance proposals.
    """
    list_display = ['voter', 'proposal', 'choice', 'created_at']
    list_filter = ['choice', 'created_at', 'proposal__world']
    search_fields = ['voter__username', 'proposal__title']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at'] 