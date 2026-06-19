from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:car_id>/', views.booking_create,  name='create'),
    path('<int:pk>/',          views.booking_detail,  name='detail'),
    path('<int:pk>/cancel/',   views.booking_cancel,  name='cancel'),
    path('<int:pk>/invoice/',  views.booking_invoice, name='invoice'),
    path('<int:pk>/review/',   views.booking_review,  name='review'),
]
