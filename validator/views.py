import random
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Device 
from .forms import DeviceRegistrationForm, DeviceAvailabilityForm

# Device registration view
def register_device(request):
    success_message = None
    if request.method == 'POST':
        form = DeviceRegistrationForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            # Hash the password before saving
            device.password = make_password(form.cleaned_data['password'])
            device.save()
            success_message = f"Device '{device.name}' with IP '{device.ip_address}' registered successfully!"
            form = DeviceRegistrationForm()
    else:
        form = DeviceRegistrationForm()

    return render(request, 'register_device.html', {'form': form, 'success_message': success_message})

# Check device availability view
def check_availability(request):
    if request.method == 'POST':
        form = DeviceAvailabilityForm(request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            password = form.cleaned_data['password']

            if not check_password(password, device.password):
                return render(request, 'check_availability.html', {'form': form, 'error': 'Incorrect Password'})

            # Simulate reachability
            reachable = "Reachable" if random.randint(0, 1) == 0 else "Not Reachable"
            return render(request, 'check_availability.html', {'form': form, 'status': reachable, 'device': device})

    else:
        form = DeviceAvailabilityForm()

    return render(request, 'check_availability.html', {'form': form})
