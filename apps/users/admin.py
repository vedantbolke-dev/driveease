"""
DriveEase Car Rental System
Users App - Admin Configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for custom user model."""

    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'is_staff', 'is_blocked', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_blocked', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']

    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'phone_number', 'address', 'city',
                'state', 'pincode', 'driving_license', 'profile_picture'
            )
        }),
        ('Account Status', {
            'fields': ('is_blocked',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number'
            )
        }),
    )

    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
        self.message_user(request, f"{queryset.count()} user(s) have been blocked.")
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
        self.message_user(request, f"{queryset.count()} user(s) have been unblocked.")
    unblock_users.short_description = "Unblock selected users"
