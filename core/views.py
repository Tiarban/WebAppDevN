# views.py - View functions for the application

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def homepage(request):
    """Render the homepage"""
    return render(request, 'core/homepage.html')

def manager_dashboard(request):
    """Render the manager dashboard"""
    return render(request, 'core/manager-dashboard.html')

def machine_detail(request, machine_id):
    """
    Render the machine detail page
    
    Args:
        machine_id: The ID of the machine to display
    """
    # In a real application, you would fetch the machine data from the database
    context = {
        'machine_id': machine_id,
        # Additional machine data would be fetched here
    }
    return render(request, 'core/machine-detail.html', context)

def assign_tech(request):
    """Render the assign technician form"""
    return render(request, 'core/assign-tech.html')

def raise_ticket(request):
    """Render the raise ticket form"""
    return render(request, 'core/raise-ticket.html')

def technician_dashboard(request):
    """Render the technician dashboard"""
    return render(request, 'core/technician-dashboard.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # In a real application, you would authenticate against Django's auth system
        # For demonstration, we'll use simple conditionals based on hardcoded values
        if email == 'manager@utensia.com' and password == 'password':
            # In a real app: user = authenticate(request, username=email, password=password)
            # login(request, user)
            return redirect('manager')
        elif email == 'tech@utensia.com' and password == 'password':
            return redirect('technician')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'core/login.html')