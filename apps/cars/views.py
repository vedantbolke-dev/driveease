"""
DriveEase Car Rental System
Cars App - Views
Handles homepage, car listing, car detail, about, and contact pages.
"""

import json
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Car, ContactMessage
from .forms import CarSearchForm


def home(request):
    """Homepage — hero, featured cars, search bar."""
    from apps.bookings.models import Review
    featured_cars = Car.objects.filter(is_available=True, is_featured=True).order_by('-created_at')[:6]
    if featured_cars.count() < 3:
        featured_cars = Car.objects.filter(is_available=True).order_by('-created_at')[:6]

    total_cars   = Car.objects.filter(is_available=True).count()
    suv_count    = Car.objects.filter(category='suv', is_available=True).count()
    luxury_count = Car.objects.filter(category='luxury', is_available=True).count()
    latest_reviews = Review.objects.select_related('user','car').order_by('-created_at')[:3]

    context = {
        'featured_cars':   featured_cars,
        'total_cars':      total_cars,
        'suv_count':       suv_count,
        'luxury_count':    luxury_count,
        'latest_reviews':  latest_reviews,
    }
    return render(request, 'home.html', context)


def car_list(request):
    """Car listing with search & filters including date availability."""
    from apps.bookings.models import Booking
    from datetime import datetime
    cars = Car.objects.all().order_by('-created_at')
    form = CarSearchForm(request.GET)

    # Date-based availability filter
    pickup_date  = request.GET.get('pickup_date', '')
    return_date  = request.GET.get('return_date', '')
    if pickup_date and return_date:
        try:
            pd = datetime.strptime(pickup_date, '%Y-%m-%d').date()
            rd = datetime.strptime(return_date, '%Y-%m-%d').date()
            if rd > pd:
                # Exclude cars that have overlapping bookings
                booked_car_ids = Booking.objects.filter(
                    status__in=['pending', 'confirmed'],
                    pickup_date__lt=rd,
                    return_date__gt=pd,
                ).values_list('car_id', flat=True)
                cars = cars.exclude(id__in=booked_car_ids)
        except ValueError:
            pass

    if form.is_valid():
        q            = form.cleaned_data.get('query')
        category     = form.cleaned_data.get('category')
        min_price    = form.cleaned_data.get('min_price')
        max_price    = form.cleaned_data.get('max_price')
        fuel_type    = form.cleaned_data.get('fuel_type')
        transmission = form.cleaned_data.get('transmission')

        if q:
            cars = cars.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
        if category:
            cars = cars.filter(category=category)
        if min_price:
            cars = cars.filter(price_per_day__gte=min_price)
        if max_price:
            cars = cars.filter(price_per_day__lte=max_price)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if transmission:
            cars = cars.filter(transmission=transmission)

    context = {
        'cars': cars,
        'form': form,
        'selected_category': request.GET.get('category', ''),
        'total_count': cars.count(),
        'pickup_date': pickup_date,
        'return_date': return_date,
        'date_filtered': bool(pickup_date and return_date),
    }
    return render(request, 'cars/car_list.html', context)


def car_detail(request, pk):
    """Car detail page with specs, blocked dates for calendar, and reviews."""
    from apps.bookings.models import Booking, Review

    car = get_object_or_404(Car, pk=pk)

    # Build list of booked date ranges so JS can block them on the date picker
    active_bookings = Booking.objects.filter(
        car=car,
        status__in=['pending', 'confirmed'],
    ).values('pickup_date', 'return_date')

    booked_ranges = [
        {
            'from': b['pickup_date'].isoformat(),
            'to':   b['return_date'].isoformat(),
        }
        for b in active_bookings
    ]

    # Reviews for this car
    reviews      = Review.objects.filter(car=car).select_related('user').order_by('-created_at')
    avg_rating   = reviews.aggregate(avg=Avg('rating'))['avg']
    review_count = reviews.count()

    similar_cars = Car.objects.filter(category=car.category, is_available=True).exclude(pk=pk)[:3]

    context = {
        'car':           car,
        'similar_cars':  similar_cars,
        'booked_ranges': json.dumps(booked_ranges),
        'reviews':       reviews,
        'avg_rating':    avg_rating,
        'review_count':  review_count,
    }
    return render(request, 'cars/car_detail.html', context)


def about(request):
    features = [
        {'title': 'User Registration & Login', 'desc': 'Secure authentication with profile management and password change'},
        {'title': 'Car Browsing & Search', 'desc': 'Search and filter cars by category, fuel type, price range and transmission'},
        {'title': 'Online Booking System', 'desc': 'Book cars with date validation, overlap prevention and cost preview'},
        {'title': 'Booking Management', 'desc': 'Users can track, view and cancel bookings from their dashboard'},
        {'title': 'Admin Dashboard', 'desc': 'Analytics with charts showing revenue, bookings and car availability'},
        {'title': 'Reviews & Ratings', 'desc': '1-5 star ratings with comments after completed bookings'},
        {'title': 'Invoice Generation', 'desc': 'Printable PDF invoice for every booking'},
        {'title': 'CSV & PDF Export', 'desc': 'Export all bookings and users as CSV or printable PDF'},
        {'title': 'Contact Form Inbox', 'desc': 'Admin receives and manages all customer contact messages'},
        {'title': 'Notification System', 'desc': 'Bell notifications for pending bookings and unread messages'},
    ]
    return render(request, 'about.html', {'features': features})


def contact(request):
    """Contact page — saves messages to DB."""
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'general').strip()
        msg     = request.POST.get('message', '').strip()

        if name and email and msg:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=msg
            )
            messages.success(
                request,
                f"Thank you, {name}! Your message has been received. We will get back to you at {email} shortly."
            )
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'contact.html')
