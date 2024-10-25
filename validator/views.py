import random
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
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
            form = DeviceRegistrationForm()  # Reset the form for new input

            # Return JSON response if requested
            if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
                return JsonResponse({
                    'message': success_message,
                    'device': {
                        'name': device.name,
                        'ip_address': device.ip_address
                    }
                }, status=201)

    else:
        form = DeviceRegistrationForm()

    # Standard HTML response
    return render(request, 'register_device.html', {'form': form, 'success_message': success_message})


# Check device availability view
def check_availability(request):
    if request.method == 'POST':
        form = DeviceAvailabilityForm(request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            password = form.cleaned_data['password']

            if not check_password(password, device.password):
                error_message = 'Incorrect Password'
                
                # Return JSON response if requested
                if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
                    return JsonResponse({'error': error_message}, status=400)

                # HTML response
                return render(request, 'check_availability.html', {'form': form, 'error': error_message})

            # Simulate reachability
            reachable = "Reachable" if random.randint(0, 1) == 0 else "Not Reachable"
            
            # JSON response if requested
            if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
                return JsonResponse({
                    'status': reachable,
                    'device': {
                        'name': device.name,
                        'ip_address': device.ip_address
                    }
                }, status=200)

            # Standard HTML response
            return render(request, 'check_availability.html', {'form': form, 'status': reachable, 'device': device})

    else:
        form = DeviceAvailabilityForm()

    # Standard HTML response
    return render(request, 'check_availability.html', {'form': form})
