from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .models import Device
from .forms import DeviceRegistrationForm

class DeviceRegistrationTests(TestCase):

    def test_add_device_json_response(self):
        """Test JSON response when a device is registered successfully."""
        data = {
            'name': 'Router1',
            'ip_address': '192.168.0.1',
            'password': 'Strongpassword123@'
        }
        
        response = self.client.post(reverse('add_device'), data, HTTP_ACCEPT='application/json')
        
        # Check that the response is JSON and contains the expected data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        json_data = response.json()
        self.assertIn('message', json_data)
        self.assertEqual(json_data['message'], "Device 'Router1' with IP '192.168.0.1' registered successfully!")
        self.assertIn('device', json_data)
        self.assertEqual(json_data['device']['name'], 'Router1')
        self.assertEqual(json_data['device']['ip_address'], '192.168.0.1')

    def test_add_device_invalid_json_response(self):
        """Test JSON response when a device registration fails due to validation errors."""
        data = {
            'name': 'abcd',  # Name is missing
            'ip_address': '192.168.0.1',
            'password': 'weak'  # Password too short
        }
        
        response = self.client.post(reverse('add_device'), data, HTTP_ACCEPT='application/json')
        
        # Check that the response is JSON and contains error messages
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn('errors', json_data)
        self.assertIn('password', json_data['errors'])


class DeviceAvailabilityTests(TestCase):

    def setUp(self):
        # Create a test device
        self.device = Device.objects.create(
            name='Router1',
            ip_address='192.168.0.1',
            password=make_password('strongpassword123')
        )

    def test_check_availability_json_response_reachable(self):
        """Test JSON response when device is reachable."""
        data = {
            'device': self.device.id,
            'password': 'strongpassword123'
        }
        
        response = self.client.post(
            reverse('check_availability'),
            data,
            HTTP_ACCEPT='application/json'
        )
        
        # Check that the response is JSON and either Reachable or Not Reachable
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn('status', json_data)
        self.assertIn(json_data['status'], ['Reachable', 'Not Reachable'])
        self.assertIn('device', json_data)
        self.assertEqual(json_data['device']['name'], self.device.name)
        self.assertEqual(json_data['device']['ip_address'], self.device.ip_address)

    def test_check_availability_json_response_incorrect_password(self):
        """Test JSON response when incorrect password is entered."""
        data = {
            'device': self.device.id,
            'password': 'wrongpassword'
        }
        
        response = self.client.post(
            reverse('check_availability'),
            data,
            HTTP_ACCEPT='application/json'
        )
        
        # Check that the response is JSON with an error message for incorrect password
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Incorrect Password')
