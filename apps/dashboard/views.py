"""
DriveEase Car Rental System
Dashboard App - Views
Admin analytics dashboard with charts and full management features.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from functools import wraps
import json

from apps.cars.models import Car
from apps.cars.forms import CarAdminForm
from apps.bookings.models import Booking

User = get_user_model()


# ── Access control helpers ────────────────────────────────────────────────────

def is_admin(user):
    """Return True only for authenticated staff/admin users."""
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    """Single decorator: requires login AND staff status."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Dashboard home ────────────────────────────────────────────────────────────

def sync_car_availability():
    """
    Auto-update car availability based on today's date vs active booking dates.
    Expired confirmed/pending bookings are auto-completed, and car availability
    is recalculated so the dashboard donut chart always reflects reality.
    """
    from datetime import date
    today = date.today()

    # Auto-complete bookings whose return_date has already passed
    expired = Booking.objects.filter(
        status__in=['confirmed', 'pending'],
        return_date__lt=today
    )
    for booking in expired:
        booking.status = 'completed'
        booking.save()

    # Cars that still have an active (future) booking
    still_rented_ids = set(
        Booking.objects.filter(
            status__in=['confirmed', 'pending'],
            return_date__gte=today
        ).values_list('car_id', flat=True)
    )

    # Bulk-update availability
    Car.objects.filter(id__in=still_rented_ids).update(is_available=False)
    Car.objects.exclude(id__in=still_rented_ids).update(is_available=True)


@admin_required
def admin_dashboard(request):
    """Main analytics dashboard with summary cards and Chart.js charts."""

    # Auto-sync car availability on every dashboard load
    sync_car_availability()

    # Summary statistics
    total_cars     = Car.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()
    rented_cars    = total_cars - available_cars
    total_users    = User.objects.filter(is_staff=False).count()
    total_bookings = Booking.objects.count()

    total_revenue = Booking.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(rev=Sum('total_cost'))['rev'] or 0

    active_rentals = Booking.objects.filter(status='confirmed').count()

    # Chart data — last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)

    monthly_revenue = (
        Booking.objects
        .filter(status__in=['confirmed', 'completed'], created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_cost'))
        .order_by('month')
    )

    monthly_bookings = (
        Booking.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    popular_cars = (
        Booking.objects
        .values('car__name', 'car__brand')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')[:5]
    )

    # Serialize chart data as JSON for Chart.js
    rev_labels   = [item['month'].strftime('%b %Y') for item in monthly_revenue]
    rev_data     = [float(item['revenue']) for item in monthly_revenue]

    booking_labels = [item['month'].strftime('%b %Y') for item in monthly_bookings]
    booking_data   = [item['count'] for item in monthly_bookings]

    popular_car_labels = [
        f"{item['car__brand']} {item['car__name']}" for item in popular_cars
    ]
    popular_car_data = [item['booking_count'] for item in popular_cars]

    # Recent activity
    recent_bookings = (
        Booking.objects
        .select_related('user', 'car')
        .order_by('-created_at')[:8]
    )
    recent_users = (
        User.objects
        .filter(is_staff=False)
        .order_by('-date_joined')[:5]
    )

    # Today stats
    today = datetime.now().date()
    today_bookings = Booking.objects.filter(created_at__date=today).count()
    today_revenue  = Booking.objects.filter(
        created_at__date=today, status__in=['confirmed','completed']
    ).aggregate(r=Sum('total_cost'))['r'] or 0

    # This month vs last month
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    this_month_rev = Booking.objects.filter(
        created_at__date__gte=this_month_start, status__in=['confirmed','completed']
    ).aggregate(r=Sum('total_cost'))['r'] or 0
    last_month_rev = Booking.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lt=this_month_start,
        status__in=['confirmed','completed']
    ).aggregate(r=Sum('total_cost'))['r'] or 0

    # Pending bookings count
    pending_count = Booking.objects.filter(status='pending').count()

    # Top 3 booked cars
    top_cars = (
        Booking.objects
        .values('car__id','car__brand','car__name','car__image','car__category')
        .annotate(count=Count('id'))
        .order_by('-count')[:3]
    )

    # Cancelled & completed stats
    completed_count  = Booking.objects.filter(status='completed').count()
    cancelled_count  = Booking.objects.filter(status='cancelled').count()

    context = {
        'total_cars':     total_cars,
        'available_cars': available_cars,
        'rented_cars':    rented_cars,
        'total_users':    total_users,
        'total_bookings': total_bookings,
        'total_revenue':  total_revenue,
        'active_rentals': active_rentals,
        'pending_count':  pending_count,
        'today_bookings': today_bookings,
        'today_revenue':  today_revenue,
        'this_month_rev': this_month_rev,
        'last_month_rev': last_month_rev,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'top_cars':       top_cars,
        'recent_bookings': recent_bookings,
        'recent_users':    recent_users,
        # Chart.js JSON data
        'rev_labels':          json.dumps(rev_labels),
        'rev_data':            json.dumps(rev_data),
        'booking_labels':      json.dumps(booking_labels),
        'booking_data':        json.dumps(booking_data),
        'popular_car_labels':  json.dumps(popular_car_labels),
        'popular_car_data':    json.dumps(popular_car_data),
        'available_cars_count': available_cars,
        'rented_cars_count':    rented_cars,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ── Car management ────────────────────────────────────────────────────────────

@admin_required
def admin_cars(request):
    """List all cars."""
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_cars.html', {'cars': cars})


@admin_required
def admin_car_add(request):
    """Add a new car."""
    if request.method == 'POST':
        form = CarAdminForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(
                request,
                f"{car.brand} {car.name} has been added successfully!"
            )
            return redirect('dashboard:cars')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CarAdminForm()

    return render(
        request,
        'dashboard/admin_car_form.html',
        {'form': form, 'action': 'Add New'}
    )


@admin_required
def admin_car_edit(request, pk):
    """Edit an existing car."""
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        form = CarAdminForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{car.brand} {car.name} has been updated successfully!"
            )
            return redirect('dashboard:cars')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CarAdminForm(instance=car)

    return render(
        request,
        'dashboard/admin_car_form.html',
        {'form': form, 'action': 'Edit', 'car': car}
    )


@admin_required
def admin_car_delete(request, pk):
    """Delete a car."""
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        car_name = f"{car.brand} {car.name}"
        car.delete()
        messages.success(request, f"{car_name} has been deleted successfully.")
        return redirect('dashboard:cars')

    return render(
        request,
        'dashboard/admin_car_delete.html',
        {'car': car}
    )


# ── Booking management ────────────────────────────────────────────────────────

@admin_required
def admin_bookings(request):
    """List all bookings — filterable by status, user, car, date range."""
    from django.db.models import Q
    status_filter = request.GET.get('status', '')
    search_query  = request.GET.get('q', '').strip()
    date_from     = request.GET.get('date_from', '')
    date_to       = request.GET.get('date_to', '')

    bookings = Booking.objects.select_related('user', 'car').order_by('-created_at')

    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if search_query:
        bookings = bookings.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)  |
            Q(user__username__icontains=search_query)   |
            Q(car__name__icontains=search_query)        |
            Q(car__brand__icontains=search_query)
        )
    if date_from:
        bookings = bookings.filter(pickup_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(pickup_date__lte=date_to)

    context = {
        'bookings':       bookings,
        'status_filter':  status_filter,
        'status_choices': Booking.STATUS_CHOICES,
        'search_query':   search_query,
        'date_from':      date_from,
        'date_to':        date_to,
        'total_count':    bookings.count(),
    }
    return render(request, 'dashboard/admin_bookings.html', context)


@admin_required
def admin_booking_update(request, pk):
    """Update booking status (admin action)."""
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        new_status  = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        valid_statuses = [s[0] for s in Booking.STATUS_CHOICES]

        if new_status in valid_statuses:
            booking.status = new_status
            booking.admin_notes = admin_notes
            booking.save()

            # Sync car availability based on booking status
            car = booking.car
            if new_status in ['confirmed', 'pending']:
                car.is_available = False
            elif new_status in ['completed', 'cancelled', 'rejected']:
                car.is_available = True
            car.save()

            messages.success(
                request,
                f"Booking #{booking.pk} status updated to '{new_status}'."
            )
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('dashboard:bookings')


# ── User management ───────────────────────────────────────────────────────────

@admin_required
def admin_users(request):
    """List all non-staff users."""
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'dashboard/admin_users.html', {'users': users})


@admin_required
def admin_user_toggle_block(request, pk):
    """Block or unblock a user account."""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.is_blocked = not user.is_blocked
        user.save()
        action = "blocked" if user.is_blocked else "unblocked"
        messages.success(request, f"User {user.username} has been {action}.")

    return redirect('dashboard:users')


@admin_required
def admin_user_delete(request, pk):
    """Delete a user account."""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' has been deleted.")
        return redirect('dashboard:users')

    return render(
        request,
        'dashboard/admin_user_delete.html',
        {'target_user': user}
    )


# ── Contact messages ──────────────────────────────────────────────────────────

@admin_required
def admin_contact_messages(request):
    """List all contact messages, mark as read."""
    from apps.cars.models import ContactMessage
    messages_qs = ContactMessage.objects.all()
    unread_count = messages_qs.filter(is_read=False).count()

    if request.method == 'POST':
        msg_id = request.POST.get('mark_read')
        if msg_id:
            ContactMessage.objects.filter(pk=msg_id).update(is_read=True)
        return redirect('dashboard:contact_messages')

    return render(request, 'dashboard/admin_contact_messages.html', {
        'messages_list': messages_qs,
        'unread_count':  unread_count,
    })


# ── CSV Export ────────────────────────────────────────────────────────────────

@admin_required
def export_bookings_csv(request):
    """Export all bookings as a CSV file."""
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="driveease_bookings.csv"'

    writer = csv.writer(response)
    writer.writerow(['Booking ID', 'User', 'Email', 'Car', 'Category',
                     'Pickup Date', 'Return Date', 'Days', 'Price/Day',
                     'Total Cost', 'Status', 'Booked On'])

    for b in Booking.objects.select_related('user', 'car').order_by('-created_at'):
        writer.writerow([
            b.pk,
            b.user.get_full_name() or b.user.username,
            b.user.email,
            f"{b.car.brand} {b.car.name}",
            b.car.get_category_display(),
            b.pickup_date,
            b.return_date,
            b.total_days,
            b.price_per_day,
            b.total_cost,
            b.get_status_display(),
            b.created_at.strftime('%d %b %Y'),
        ])

    return response


@admin_required
def export_users_csv(request):
    """Export all users as CSV."""
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="driveease_users.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Full Name', 'Username', 'Email', 'Phone',
                     'City', 'Joined On', 'Bookings', 'Status'])

    for u in User.objects.filter(is_staff=False).order_by('-date_joined'):
        writer.writerow([
            u.pk,
            u.get_full_name(),
            u.username,
            u.email,
            u.phone_number or '',
            u.city or '',
            u.date_joined.strftime('%d %b %Y'),
            u.bookings.count(),
            'Blocked' if u.is_blocked else 'Active',
        ])

    return response


# ── PDF Export ────────────────────────────────────────────────────────────────

@admin_required
def export_bookings_pdf(request):
    """Export all bookings as a styled PDF using pure HTML→PDF via weasyprint or fallback to HTML."""
    from django.template.loader import render_to_string
    bookings = Booking.objects.select_related('user', 'car').order_by('-created_at')
    total_revenue = bookings.filter(status__in=['confirmed','completed']).aggregate(t=Sum('total_cost'))['t'] or 0

    try:
        import weasyprint
        html_string = render_to_string('dashboard/export_bookings_pdf.html', {
            'bookings': bookings, 'total_revenue': total_revenue
        })
        pdf = weasyprint.HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="driveease_bookings.pdf"'
        return response
    except ImportError:
        # Weasyprint not installed - serve as printable HTML page
        return render(request, 'dashboard/export_bookings_pdf.html', {
            'bookings': bookings, 'total_revenue': total_revenue, 'print_mode': True
        })


@admin_required  
def export_users_pdf(request):
    """Export all users as PDF."""
    from django.template.loader import render_to_string
    users = User.objects.filter(is_staff=False).order_by('-date_joined')

    try:
        import weasyprint
        html_string = render_to_string('dashboard/export_users_pdf.html', {'users': users})
        pdf = weasyprint.HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="driveease_users.pdf"'
        return response
    except ImportError:
        return render(request, 'dashboard/export_users_pdf.html', {
            'users': users, 'print_mode': True
        })


# ── Admin Reports ─────────────────────────────────────────────────────────────

@admin_required
def admin_reports(request):
    """Comprehensive reports page with revenue, bookings, top cars."""
    from datetime import datetime, timedelta

    today = datetime.now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)

    # This month stats
    this_month_bookings = Booking.objects.filter(created_at__date__gte=this_month_start)
    this_month_revenue  = this_month_bookings.filter(
        status__in=['confirmed','completed']
    ).aggregate(t=Sum('total_cost'))['t'] or 0

    # Last month stats
    last_month_bookings = Booking.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lt=this_month_start
    )
    last_month_revenue = last_month_bookings.filter(
        status__in=['confirmed','completed']
    ).aggregate(t=Sum('total_cost'))['t'] or 0

    # Top 5 most booked cars
    top_cars = (
        Booking.objects
        .values('car__brand', 'car__name', 'car__category')
        .annotate(count=Count('id'), revenue=Sum('total_cost'))
        .order_by('-count')[:5]
    )

    # Status breakdown
    status_breakdown = (
        Booking.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Category revenue
    category_revenue = (
        Booking.objects
        .filter(status__in=['confirmed','completed'])
        .values('car__category')
        .annotate(revenue=Sum('total_cost'), count=Count('id'))
        .order_by('-revenue')
    )

    # Monthly data for last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_data = (
        Booking.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            count=Count('id'),
            revenue=Sum('total_cost')
        )
        .order_by('month')
    )

    context = {
        'this_month_revenue':   this_month_revenue,
        'this_month_count':     this_month_bookings.count(),
        'last_month_revenue':   last_month_revenue,
        'last_month_count':     last_month_bookings.count(),
        'total_revenue':        Booking.objects.filter(status__in=['confirmed','completed']).aggregate(t=Sum('total_cost'))['t'] or 0,
        'total_bookings':       Booking.objects.count(),
        'top_cars':             top_cars,
        'status_breakdown':     status_breakdown,
        'category_revenue':     category_revenue,
        'monthly_data':         list(monthly_data),
        'monthly_labels':       [m['month'].strftime('%b %Y') for m in monthly_data],
        'monthly_counts':       [m['count'] for m in monthly_data],
        'monthly_revenues':     [float(m['revenue'] or 0) for m in monthly_data],
    }
    return render(request, 'dashboard/admin_reports.html', context)


# ── Pending bookings count for notification bell ──────────────────────────────

def get_pending_count():
    return Booking.objects.filter(status='pending').count()

