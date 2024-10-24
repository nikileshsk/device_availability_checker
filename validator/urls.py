from django.urls import path
from .views import register_device, check_availability

urlpatterns = [
    path('register/', register_device, name='register_device'),
    path('check/', check_availability, name='check_availability'),
]
