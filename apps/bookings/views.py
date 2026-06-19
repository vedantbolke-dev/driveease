"""
DriveEase Car Rental System
Bookings App - Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from apps.cars.models import Car
from .models import Booking, Review
from .forms import BookingForm, ReviewForm


@login_required
def booking_create(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if not car.is_available:
        messages.error(request, f"Sorry, {car.brand} {car.name} is currently not available for booking.")
        return redirect('cars:detail', pk=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, car=car)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user          = request.user
            booking.car           = car
            booking.price_per_day = car.price_per_day
            booking.pickup_location = form.cleaned_data.get('pickup_location', car.location)
            booking.status        = 'pending'
            booking.save()

            car.is_available = False
            car.save()

            messages.success(request, f"Booking confirmed! Booking #{booking.pk} is pending approval.")
            return redirect('bookings:detail', pk=booking.pk)
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = BookingForm(car=car, initial={'pickup_location': car.location})

    return render(request, 'bookings/booking_form.html', {'form': form, 'car': car})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    # Check if review already exists
    has_review = hasattr(booking, 'review')
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'has_review': has_review,
    })


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        if booking.can_cancel():
            booking.status = 'cancelled'
            booking.save()
            booking.car.is_available = True
            booking.car.save()
            messages.success(request, f"Booking #{booking.pk} has been cancelled successfully.")
        else:
            messages.error(request, f"Booking #{booking.pk} cannot be cancelled at this stage.")
        return redirect('users:dashboard')

    return render(request, 'bookings/booking_cancel_confirm.html', {'booking': booking})


@login_required
def booking_invoice(request, pk):
    """Printable invoice for a booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/invoice.html', {'booking': booking})


@login_required
def booking_review(request, pk):
    """Submit a star review after a completed booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status != 'completed':
        messages.error(request, "You can only review completed bookings.")
        return redirect('bookings:detail', pk=pk)

    if hasattr(booking, 'review'):
        messages.info(request, "You have already reviewed this booking.")
        return redirect('bookings:detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.user    = request.user
            review.car     = booking.car
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('bookings:detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'bookings/review_form.html', {'form': form, 'booking': booking})
