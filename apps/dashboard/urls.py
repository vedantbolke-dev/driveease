from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='home'),

    # Car management
    path('cars/',                 views.admin_cars,       name='cars'),
    path('cars/add/',             views.admin_car_add,    name='car_add'),
    path('cars/<int:pk>/edit/',   views.admin_car_edit,   name='car_edit'),
    path('cars/<int:pk>/delete/', views.admin_car_delete, name='car_delete'),

    # Booking management
    path('bookings/',                  views.admin_bookings,       name='bookings'),
    path('bookings/<int:pk>/update/',  views.admin_booking_update, name='booking_update'),
    path('bookings/export/csv/',       views.export_bookings_csv,  name='export_bookings_csv'),
    path('bookings/export/pdf/',       views.export_bookings_pdf,  name='export_bookings_pdf'),

    # User management
    path('users/',                       views.admin_users,             name='users'),
    path('users/<int:pk>/toggle-block/', views.admin_user_toggle_block, name='user_toggle_block'),
    path('users/<int:pk>/delete/',       views.admin_user_delete,       name='user_delete'),
    path('users/export/csv/',            views.export_users_csv,        name='export_users_csv'),
    path('users/export/pdf/',            views.export_users_pdf,        name='export_users_pdf'),

    # Contact messages
    path('messages/', views.admin_contact_messages, name='contact_messages'),

    # Reports
    path('reports/', views.admin_reports, name='reports'),
]
