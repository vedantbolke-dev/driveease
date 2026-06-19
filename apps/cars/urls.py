"""
DriveEase Car Rental System
Cars App - URL Configuration
"""

from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='list'),
    path('<int:pk>/', views.car_detail, name='detail'),
]
