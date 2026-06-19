"""
DriveEase Car Rental System
Users App - Views
Handles registration, login, logout, user dashboard, and profile.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Sum

from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm

User = get_user_model()


def register_view(request):
    """
    Handle new user registration.
    GET:  Show registration form.
    POST: Create user and redirect to login.
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Account created successfully! Welcome, {user.first_name}! "
                f"Please log in to continue."
            )
            return redirect('users:login')
        else:
            messages.error(
                request,
                "Registration failed. Please fix the errors below."
            )
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    GET:  Show login form.
    POST: Authenticate and login user.
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Block access for blocked accounts
                if user.is_blocked:
                    messages.error(
                        request,
                        "Your account has been blocked. "
                        "Please contact support@driveease.com"
                    )
                    return render(request, 'users/login.html', {'form': form})

                login(request, user)
                messages.success(
                    request,
                    f"Welcome back, {user.first_name or user.username}!"
                )

                next_url = request.GET.get('next', 'users:dashboard')
                return redirect(next_url)
        else:
            messages.error(
                request,
                "Invalid username or password. Please try again."
            )
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard_view(request):
    """
    User dashboard — booking history, active rentals, total spend.
    """
    from apps.bookings.models import Booking   # local import avoids circular

    all_bookings = Booking.objects.filter(
        user=request.user
    ).select_related('car').order_by('-created_at')

    active_bookings    = all_bookings.filter(status__in=['pending', 'confirmed'])
    completed_bookings = all_bookings.filter(status='completed')
    cancelled_bookings = all_bookings.filter(status='cancelled')

    # Aggregate total spend using DB-level sum (uses correct field name)
    total_spent = completed_bookings.aggregate(
        total=Sum('total_cost')
    )['total'] or 0

    context = {
        'all_bookings':        all_bookings,
        'active_bookings':     active_bookings,
        'completed_bookings':  completed_bookings,
        'cancelled_bookings':  cancelled_bookings,
        'total_spent':         total_spent,
        'bookings_count':      all_bookings.count(),
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    """
    View and update user profile.
    GET:  Show profile form.
    POST: Save profile changes.
    """
    if request.method == 'POST':
        form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile has been updated successfully!"
            )
            return redirect('users:profile')
        else:
            messages.error(
                request,
                "Failed to update profile. Please fix the errors."
            )
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def password_change_view(request):
    """Allow user to change their password."""
    from django.contrib.auth import update_session_auth_hash
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        elif len(new_password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully!")
            return redirect('users:profile')

    return render(request, 'users/password_change.html')
