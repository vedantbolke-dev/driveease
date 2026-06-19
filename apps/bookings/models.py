"""
DriveEase Car Rental System
Bookings App - Models
Handles car bookings with status tracking and cost calculation.
"""

from django.db import models
from django.conf import settings
from apps.cars.models import Car
from datetime import date


class Booking(models.Model):
    """
    Represents a car rental booking made by a user.
    Tracks dates, cost, and booking status.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # Booking details
    pickup_date = models.DateField(verbose_name="Pickup Date")
    return_date = models.DateField(verbose_name="Return Date")
    pickup_location = models.CharField(
        max_length=200,
        default='Newasa, Maharashtra',
        verbose_name="Pickup Location"
    )
    drop_location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Drop Location"
    )

    # Pricing
    total_days = models.PositiveIntegerField(
        default=1,
        verbose_name="Total Days"
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price Per Day (₹)"
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total Cost (₹)"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Booking Status"
    )

    # Additional info
    special_requests = models.TextField(
        blank=True,
        verbose_name="Special Requests"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Admin Notes"
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Booked On"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Booking #{self.pk} - {self.user.username} "
            f"| {self.car.name} | {self.pickup_date}"
        )

    def save(self, *args, **kwargs):
        """Auto-calculate total days and cost before saving."""
        if self.pickup_date and self.return_date:
            delta = self.return_date - self.pickup_date
            self.total_days = delta.days if delta.days > 0 else 1

        if self.price_per_day:
            self.total_cost = self.price_per_day * self.total_days

        super().save(*args, **kwargs)

    def can_cancel(self):
        """Check if booking can be cancelled (only pending/confirmed)."""
        return self.status in ['pending', 'confirmed']

    def get_status_badge_class(self):
        """Returns Bootstrap badge class for status."""
        badge_map = {
            'pending': 'bg-warning text-dark',
            'confirmed': 'bg-success',
            'completed': 'bg-secondary',
            'cancelled': 'bg-danger',
            'rejected': 'bg-dark',
        }
        return badge_map.get(self.status, 'bg-secondary')

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']


class Review(models.Model):
    """Star rating + comment left by a user after a completed booking."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='review'
    )
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name='reviews'
    )
    car = models.ForeignKey(
        'cars.Car', on_delete=models.CASCADE, related_name='reviews'
    )
    rating  = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.car.brand} {self.car.name} — {self.rating}★"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
