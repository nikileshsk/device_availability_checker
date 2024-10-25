from django.urls import path
from .views import add_device, check_availability

urlpatterns = [
    path('add_device/', add_device, name='add_device'),
    path('check_availability/', check_availability, name='check_availability'),
]
