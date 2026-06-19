"""
DriveEase Car Rental System
Users App - Models
Custom user model with extended profile fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model with additional fields for car rental system.
    Inherits from Django's AbstractUser for built-in auth features.
    """

    # Contact information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # Profile picture
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # Driving license
    driving_license = models.CharField(max_length=50, blank=True, null=True)

    # Account status
    is_blocked = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_active_bookings_count(self):
        """Returns count of active/pending bookings for this user."""
        return self.bookings.filter(
            status__in=['pending', 'confirmed']
        ).count()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
