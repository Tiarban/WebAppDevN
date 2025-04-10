# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
<<<<<<< HEAD
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from .models import User, Machine, Ticket, TicketUpdate, TechnicianAssignment, MachineWarning
from .forms import (
    LoginForm, MachineForm, TicketForm, TicketUpdateForm, 
    TechnicianAssignmentForm, MachineWarningForm
)
=======
from django.contrib.auth.models import Group, User 
from rest_framework import permissions, viewsets

from core.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    #user api endpoint
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    #group api endpoint
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
>>>>>>> 2ec26a5b8867a6199b67ce2d7a55de2ee365478c

# User type checks
def is_manager(user):
    return user.is_authenticated and user.user_type == 'manager'

def is_technician(user):
    return user.is_authenticated and user.user_type == 'technician'

# Authentication views
def homepage(request):
    """Public homepage view"""
    return render(request, 'core/homepage.html')

def login_view(request):
    """Login view for all users"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.user_type == 'manager':
                    return redirect('manager')
                elif user.user_type == 'technician':
                    return redirect('technician')
                else:
                    return redirect('homepage')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
                
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    """Logout view for all users"""
    logout(request)
    return redirect('login')

# Manager views
@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    """Dashboard view for managers"""
    # Count machines by status
    status_counts = Machine.objects.values('status').annotate(count=Count('status'))
    status_dict = {item['status']: item['count'] for item in status_counts}
    
    # Get all machines
    machines = Machine.objects.all().order_by('code')
    
    context = {
        'ok_count': status_dict.get('ok', 0),
        'warning_count': status_dict.get('warning', 0),
        'fault_count': status_dict.get('fault', 0),
        'machines': machines,
    }
    
    return render(request, 'core/manager-dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def assign_technician(request):
    """View for assigning technicians to machines"""
    if request.method == 'POST':
        form = TechnicianAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            
            # If this is for a ticket, update the ticket
            ticket_id = request.POST.get('ticket_id')
            if ticket_id:
                ticket = get_object_or_404(Ticket, id=ticket_id)
                ticket.assigned_to = assignment.technician
                ticket.status = 'assigned'
                ticket.save()
                
                # Create ticket update
                TicketUpdate.objects.create(
                    ticket=ticket, 
                    user=request.user, 
                    update_text=f"Assigned to {assignment.technician.first_name} {assignment.technician.last_name}"
                )
                
                messages.success(request, 'Technician assigned and ticket updated!')
                return redirect('machine-detail', machine_id=assignment.machine.id)
            else:
                messages.success(request, 'Technician assigned successfully!')
                return redirect('manager')
    else:
        # Pre-fill machine if specified in URL
        machine_id = request.GET.get('machine_id')
        ticket_id = request.GET.get('ticket_id')
        initial = {}
        
        if machine_id:
            initial['machine'] = machine_id
        
        form = TechnicianAssignmentForm(initial=initial)
    
    context = {
        'form': form,
        'ticket_id': ticket_id,
    }
    
    return render(request, 'core/assign-tech.html', context)

@login_required
@user_passes_test(is_manager)
def add_machine(request):
    """View for adding a new machine"""
    if request.method == 'POST':
        form = MachineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Machine added successfully!')
            return redirect('manager')
    else:
        form = MachineForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/add-machine.html', context)

@login_required
@user_passes_test(is_manager)
def edit_machine(request, machine_id):
    """View for editing a machine"""
    machine = get_object_or_404(Machine, pk=machine_id)
    
    if request.method == 'POST':
        form = MachineForm(request.POST, request.FILES, instance=machine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Machine updated successfully!')
            return redirect('machine-detail', machine_id=machine.id)
    else:
        form = MachineForm(instance=machine)
    
    context = {
        'form': form,
        'machine': machine,
    }
    
    return render(request, 'core/edit_machine.html', context)

@login_required
@user_passes_test(is_manager)
def generate_report(request):
    """View for generating a machine status report"""
    machines = Machine.objects.all()
    open_tickets = Ticket.objects.filter(status__in=['open', 'assigned', 'in_progress'])
    
    context = {
        'machines': machines,
        'open_tickets': open_tickets,
        'generated_at': timezone.now(),
    }
    
    return render(request, 'core/generate-report.html', context)

# Technician views
@login_required
@user_passes_test(is_technician)
def technician_dashboard(request):
    """Dashboard view for technicians"""
    # Get all machines, same as manager dashboard
    machines = Machine.objects.all().order_by('code')
    
    # Get open tickets for assigned machines
    open_tickets = Ticket.objects.filter(
        status__in=['open', 'assigned', 'in_progress']
    ).order_by('-created_at')
    
    context = {
        'machines': machines,
        'tickets': open_tickets,
    }
    
    return render(request, 'core/technician-dashboard.html', context)

# Shared views
@login_required
def machine_detail(request, machine_id):
    """Detail view for a specific machine"""
    machine = get_object_or_404(Machine, pk=machine_id)
    tickets = Ticket.objects.filter(machine=machine).order_by('-created_at')
    
    context = {
        'machine': machine,
        'tickets': tickets,
    }
    
    return render(request, 'core/machine-detail.html', context)

@login_required
def raise_ticket(request):
    """View for raising a fault ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            
            # Show success message
            messages.success(request, f'Ticket {ticket.fault_code} created successfully!')
            
            return redirect('machine-detail', machine_id=ticket.machine.id)
    else:
        # Pre-fill machine if specified in URL
        machine_id = request.GET.get('machine_id')
        initial = {}
        
        if machine_id:
            initial['machine'] = machine_id
            
        form = TicketForm(initial=initial)
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/raise-ticket.html', context)

@login_required
def add_warning(request, machine_id):
    """View for adding a warning to a machine"""
    machine = get_object_or_404(Machine, pk=machine_id)
    
    if request.method == 'POST':
        form = MachineWarningForm(request.POST, request.FILES)
        if form.is_valid():
            warning = form.save(commit=False)
            warning.machine = machine
            warning.added_by = request.user
            warning.save()
            
            # Update machine status to warning handled in model save method
            
            messages.success(request, 'Warning added successfully!')
            return redirect('machine-detail', machine_id=machine.id)
    else:
        form = MachineWarningForm()
    
    context = {
        'form': form,
        'machine': machine,
    }
    
    return render(request, 'core/add-warning.html', context)

@login_required
def update_ticket(request, ticket_id):
    """View for updating a ticket status"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.ticket = ticket
            update.user = request.user
            update.save()
            
            # Update ticket status if provided
            new_status = request.POST.get('ticket_status')
            if new_status and new_status in dict(Ticket.STATUS_CHOICES):
                old_status = ticket.status
                ticket.status = new_status
                ticket.save()
                
                # If ticket is resolved, update machine status
                if new_status == 'resolved':
                    machine = ticket.machine
                    # Only update if no other open tickets
                    if not Ticket.objects.filter(machine=machine).exclude(id=ticket.id).filter(status__in=['open', 'assigned', 'in_progress']).exists():
                        machine.status = 'ok'
                        machine.update_text = 'Resolved'
                        machine.warning_text = None
                        machine.save()
                        
                # Log the status change
                if old_status != new_status:
                    status_update = f"Status changed from {dict(Ticket.STATUS_CHOICES)[old_status]} to {dict(Ticket.STATUS_CHOICES)[new_status]}"
                    TicketUpdate.objects.create(
                        ticket=ticket,
                        user=request.user,
                        update_text=status_update
                    )
            
            messages.success(request, 'Ticket updated successfully!')
            return redirect('machine-detail', machine_id=ticket.machine.id)
    else:
        form = TicketUpdateForm()
    
    # Get ticket updates
    updates = ticket.updates.all()
    
    context = {
        'form': form,
        'ticket': ticket,
        'updates': updates,
    }
    
    return render(request, 'core/update-ticket.html', context)


def about_us(request):
    return render(request, 'core/about.html')

def careers(request):
    return render(request, 'core/careers.html')

def contact(request):
    return render(request, 'core/contact.html')

def products(request):
    return render(request, 'core/products.html')