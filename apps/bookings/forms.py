"""
DriveEase Car Rental System
Bookings App - Forms
"""

from django import forms
from .models import Booking, Review
from datetime import date


class BookingForm(forms.ModelForm):
    pickup_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        }),
        label='Pickup Date'
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        }),
        label='Return Date'
    )
    pickup_location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Newasa, Maharashtra'
        }),
        label='Pickup Location'
    )
    drop_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Same as pickup location (optional)'
        }),
        label='Drop Location (Optional)'
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special requests or requirements...'
        }),
        label='Special Requests (Optional)'
    )

    class Meta:
        model = Booking
        fields = ['pickup_date', 'return_date', 'pickup_location', 'drop_location', 'special_requests']

    def __init__(self, *args, car=None, **kwargs):
        self.car = car
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pickup  = cleaned_data.get('pickup_date')
        return_d = cleaned_data.get('return_date')
        today   = date.today()

        if pickup and pickup < today:
            raise forms.ValidationError("Pickup date cannot be in the past.")

        if pickup and return_d:
            if return_d <= pickup:
                raise forms.ValidationError("Return date must be after the pickup date.")

            days = (return_d - pickup).days
            if days > 90:
                raise forms.ValidationError("Maximum rental period is 90 days.")

            if self.car:
                overlapping = Booking.objects.filter(
                    car=self.car,
                    status__in=['pending', 'confirmed'],
                    pickup_date__lt=return_d,
                    return_date__gt=pickup,
                )
                if self.instance and self.instance.pk:
                    overlapping = overlapping.exclude(pk=self.instance.pk)
                if overlapping.exists():
                    raise forms.ValidationError(
                        "This car is already booked for the selected dates. "
                        "Please choose different dates."
                    )

        return cleaned_data


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f'{i} Star' + ('s' if i > 1 else '')) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label='Your Rating'
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Share your experience with this car...'
        }),
        label='Your Review (Optional)'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
