"""
DriveEase Car Rental System - Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.cars import views as car_views

urlpatterns = [
    # Django built-in admin
    path('admin/', admin.site.urls),

    # Home page
    path('', car_views.home, name='home'),

    # About & Contact pages
    path('about/', car_views.about, name='about'),
    path('contact/', car_views.contact, name='contact'),

    # User authentication and dashboard
    path('users/', include('apps.users.urls', namespace='users')),

    # Car listings and details
    path('cars/', include('apps.cars.urls', namespace='cars')),

    # Booking system
    path('bookings/', include('apps.bookings.urls', namespace='bookings')),

    # Admin analytics dashboard
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # Password reset (Django built-in)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site titles
admin.site.site_header = "DriveEase Administration"
admin.site.site_title = "DriveEase Admin Portal"
admin.site.index_title = "Welcome to DriveEase Admin Panel"
