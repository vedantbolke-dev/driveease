from django.contrib import admin
from .models import Car, ContactMessage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display  = ('brand', 'name', 'category', 'price_per_day', 'is_available', 'is_featured')
    list_filter   = ('category', 'fuel_type', 'is_available', 'is_featured')
    search_fields = ('name', 'brand')
    list_editable = ('is_available', 'is_featured')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter   = ('is_read', 'subject')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
