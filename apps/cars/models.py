"""
DriveEase Car Rental System
Cars App - Models
Car listings, categories, and availability tracking.
"""

from django.db import models


class Car(models.Model):
    """
    Represents a car available for rent in the DriveEase system.
    Stores all car details including pricing, specs, and availability.
    """

    # Category choices
    CATEGORY_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('luxury', 'Luxury'),
    ]

    # Fuel type choices
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    # Transmission choices
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    # Basic car information
    name = models.CharField(max_length=100, verbose_name="Car Name")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model_year = models.PositiveIntegerField(verbose_name="Model Year")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='sedan',
        verbose_name="Category"
    )

    # Car specifications
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        default='petrol'
    )
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='manual'
    )
    seating_capacity = models.PositiveIntegerField(default=5)
    mileage = models.CharField(
        max_length=30,
        blank=True,
        help_text="e.g., 18 km/l"
    )
    engine_cc = models.CharField(
        max_length=30,
        blank=True,
        help_text="e.g., 1200cc"
    )
    color = models.CharField(max_length=50, blank=True)

    # Pricing (in Indian Rupees)
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price Per Day (₹)"
    )

    # Description
    description = models.TextField(blank=True, verbose_name="Description")
    features = models.TextField(
        blank=True,
        help_text="Enter features separated by commas"
    )

    # Images
    image = models.ImageField(
        upload_to='cars/',
        blank=True,
        null=True,
        verbose_name="Car Image"
    )

    # Availability
    is_available = models.BooleanField(default=True, verbose_name="Available")
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured on Homepage"
    )

    # Location
    location = models.CharField(
        max_length=200,
        default='Newasa, Maharashtra',
        verbose_name="Pickup Location"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})"

    def get_features_list(self):
        """Returns features as a list."""
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        ordering = ['-created_at']


class ContactMessage(models.Model):
    """Stores messages submitted via the Contact Us page."""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('booking', 'Booking Help'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]

    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    phone   = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.created_at.strftime('%d %b %Y')})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
