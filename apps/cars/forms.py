"""
DriveEase Car Rental System
Cars App - Forms
Car search and admin car management forms.
"""

from django import forms
from .models import Car


class CarSearchForm(forms.Form):
    """
    Search and filter form for car listings.
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search cars by name or brand...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Car.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min ₹',
            'min': 0
        })
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max ₹',
            'min': 0
        })
    )
    fuel_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Fuel Types')] + Car.FUEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    transmission = forms.ChoiceField(
        required=False,
        choices=[('', 'All Transmission')] + Car.TRANSMISSION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class CarAdminForm(forms.ModelForm):
    """
    Admin form for adding and editing cars.
    """
    class Meta:
        model = Car
        fields = [
            'name', 'brand', 'model_year', 'category',
            'fuel_type', 'transmission', 'seating_capacity',
            'mileage', 'engine_cc', 'color',
            'price_per_day', 'description', 'features',
            'image', 'is_available', 'is_featured', 'location'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model_year': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 2000, 'max': 2030
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'seating_capacity': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 2, 'max': 10
            }),
            'mileage': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g., 18 km/l'
            }),
            'engine_cc': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g., 1200cc'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g., White'
            }),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'placeholder': 'Price in ₹'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'AC, Power Steering, ABS, Airbags, ...'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
