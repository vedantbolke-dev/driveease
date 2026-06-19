/*
 * DriveEase Car Rental System - Main JavaScript
 * Developed by: Vedant Rajendra Bolke & Vishal Rajendra Hapse
 * B.Sc. Computer Science | Shri Dnyaneshwar Mahavidyalaya, Newasa
 */

"use strict";

// ===== Navbar scroll effect =====
window.addEventListener('scroll', function () {
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// ===== Auto-dismiss flash messages after 4 seconds =====
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });
});

// ===== Smooth scrolling for anchor links =====
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== Booking form: set minimum return date based on pickup date =====
document.addEventListener('DOMContentLoaded', function () {
    const pickupInput = document.querySelector('[name="pickup_date"]');
    const returnInput = document.querySelector('[name="return_date"]');

    if (pickupInput && returnInput) {
        // Set today as minimum pickup date
        const today = new Date().toISOString().split('T')[0];
        pickupInput.min = today;
        returnInput.min = today;

        pickupInput.addEventListener('change', function () {
            const nextDay = new Date(this.value);
            nextDay.setDate(nextDay.getDate() + 1);
            returnInput.min = nextDay.toISOString().split('T')[0];
            if (returnInput.value && returnInput.value <= this.value) {
                returnInput.value = '';
            }
        });
    }
});

// ===== Image preview before upload (profile/car image forms) =====
document.addEventListener('DOMContentLoaded', function () {
    const imageInputs = document.querySelectorAll('input[type="file"][name="image"], input[type="file"][name="profile_picture"]');
    imageInputs.forEach(function (input) {
        input.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file) return;

            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
            if (!allowedTypes.includes(file.type)) {
                alert('Please upload a valid image (JPEG, PNG, or WebP).');
                input.value = '';
                return;
            }

            if (file.size > 5 * 1024 * 1024) {
                alert('Image size must be less than 5MB.');
                input.value = '';
                return;
            }
        });
    });
});

// ===== Confirm delete actions =====
document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
        const msg = this.getAttribute('data-confirm') || 'Are you sure?';
        if (!confirm(msg)) e.preventDefault();
    });
});

// ===== Admin: Booking status color feedback =====
document.addEventListener('DOMContentLoaded', function () {
    const statusSelects = document.querySelectorAll('select[name="status"]');
    statusSelects.forEach(function (sel) {
        sel.addEventListener('change', function () {
            const colors = {
                'pending': '#ffc107',
                'confirmed': '#198754',
                'completed': '#6c757d',
                'cancelled': '#dc3545',
                'rejected': '#212529'
            };
            sel.style.borderColor = colors[sel.value] || '#dee2e6';
        });
    });
});

// ===== Car price live calculator on car listing hover =====
document.addEventListener('DOMContentLoaded', function () {
    // Animate stats counter on scroll (homepage)
    const statElements = document.querySelectorAll('.hero-stat-number');

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                // Just a visual trigger - numbers are already set
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.5 });

    statElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(10px)';
        el.style.transition = 'all 0.5s ease';
        observer.observe(el);
    });
});

// ===== Tooltip initialization for Bootstrap 5 =====
document.addEventListener('DOMContentLoaded', function () {
    const tooltipEls = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipEls.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });
});
