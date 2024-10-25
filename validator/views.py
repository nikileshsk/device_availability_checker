import random
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import Device
from .forms import DeviceRegistrationForm, DeviceAvailabilityForm

# Device registration view
def add_device(request):
    success_message = None
    error_messages = []
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
            # Collect form errors for display
            error_messages = form.errors.as_json() if request.headers.get('Accept') == 'application/json' else form.errors
            if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
                return JsonResponse({'errors': error_messages}, status=400)

    else:
        form = DeviceRegistrationForm()

    # Standard HTML response with success and error messages
    return render(request, 'add_device.html', {
        'form': form,
        'success_message': success_message,
        'error_messages': error_messages,
    })


# Check device availability view
def check_availability(request):
    error_message = None
    status_message = None
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

            else:
                # Simulate reachability
                status_message = "Reachable" if random.randint(0, 1) == 0 else "Not Reachable"
                
                # JSON response if requested
                if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
                    return JsonResponse({
                        'status': status_message,
                        'device': {
                            'name': device.name,
                            'ip_address': device.ip_address
                        }
                    }, status=200)

        else:
            # Collect form errors for display
            error_message = form.errors.as_json() if request.headers.get('Accept') == 'application/json' else form.errors

    else:
        form = DeviceAvailabilityForm()

    # Standard HTML response with error or status message
    return render(request, 'check_availability.html', {
        'form': form,
        'error': error_message,
        'status': status_message,
    })
