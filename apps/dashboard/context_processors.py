from apps.cars.models import ContactMessage
from apps.bookings.models import Booking

def unread_messages(request):
    """Inject unread message count and pending bookings into all admin templates."""
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'unread_messages_count': ContactMessage.objects.filter(is_read=False).count(),
            'pending_bookings_count': Booking.objects.filter(status='pending').count(),
        }
    return {'unread_messages_count': 0, 'pending_bookings_count': 0}
