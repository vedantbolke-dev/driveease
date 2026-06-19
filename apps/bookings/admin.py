from django.contrib import admin
from .models import Booking, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'user', 'car', 'pickup_date', 'return_date', 'total_cost', 'status')
    list_filter   = ('status',)
    search_fields = ('user__username', 'car__name', 'car__brand')
    list_select_related = ('user', 'car')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('user', 'car', 'rating', 'created_at')
    list_filter   = ('rating',)
    search_fields = ('user__username', 'car__name')
    list_select_related = ('user', 'car', 'booking')
