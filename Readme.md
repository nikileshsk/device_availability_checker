# Device Registration App

A simple Django application for registering and checking the availability of network devices.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment (Optional but Recommended)](#2-create-a-virtual-environment-optional-but-recommended)
  - [3. Install Required Packages](#3-install-required-packages)
  - [4. Run Database Migrations](#4-run-database-migrations)
  - [5. Create a Superuser (Optional)](#5-create-a-superuser-optional)
  - [6. Start the Development Server](#6-start-the-development-server)
  - [7. Access the Application](#7-access-the-application)
- [Endpoints](#endpoints)
  - [1. Device Registration](#1-device-registration)
  - [2. Check Device Availability](#2-check-device-availability)
  
## Features

- Register new devices with a name, IP address, and password.
- Check the availability of registered devices.
- Passwords are securely hashed before storage.

## Technologies Used

- Python
- Django
- SQLite3 (default database)

## Setup

### 1. Clone the Repository

Clone the repository from GitHub:

```
git clone https://github.com/nikileshsk/device_availability_checker.git
cd device_availability_checker
```
### 2. Create a Virtual Environment (Optional but Recommended)
It is recommended to create a virtual environment to isolate dependencies:
you can run the below command on windows
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Required Packages
Install the required packages listed in requirements.txt:

```
pip install -r requirements.txt
```

### 4. Run Database Migrations
Initialize the database and create the necessary tables:
```
python manage.py migrate
```

### 5. Create a Superuser (Optional)
You can create a superuser to access the Django admin panel:
```
python manage.py createsuperuser
```

### 6. Start the Development Server
Run the Django development server:
```
python manage.py runserver
```

7. Access the Application
Open your browser and go to http://127.0.0.1:8000/add_device to access the application.

### Endpoints
1. Device Registration

```
Endpoint: /add_device

Method: POST

Request Payload:

json

{
    "name": "Router1",
    "ip_address": "192.168.0.1",
    "password": "StrongPassword123"
}
Success Response:

Code: 201 Created
Response Body:
json

{
    "message": "Device 'Router1' with IP '192.168.0.1' registered successfully!",
    "device": {
        "name": "Router1",
        "ip_address": "192.168.0.1"
    }
}
Error Response (for invalid input):

Code: 400 Bad Request
Response Body:
json

{
    "error": "custom Field validation errors for every field."
}
```
2. Check Device Availability
Endpoint: /check_availability

```
Method: POST

Request Payload:

json

{
    "device": "Router1",  // The device name to check
    "password": "StrongPassword123"
}
Success Response:

Code: 200 OK
Response Body:
json

{
    "status": "Reachable",
    "device": {
        "name": "Router1",
        "ip_address": "192.168.0.1"
    }
}
Error Responses:

Code: 400 Bad Request (for incorrect password):

json

{
    "error": "Incorrect Password"
}
Code: 404 Not Found (for non-existing device):

json

{
    "error": "Device not found."
}
```