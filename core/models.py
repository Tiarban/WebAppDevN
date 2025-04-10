# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPES = (
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('guest', 'Guest'),
        ('admin', 'Admin'),
    )
    
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='guest')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_user_type_display()})"

class Machine(models.Model):
    STATUS_CHOICES = (
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('fault', 'Fault'),
    )
    
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ok')
    update_text = models.CharField(max_length=255, default='Working Fine')
    warning_text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='machines/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    fault_code = models.CharField(max_length=20, unique=True, editable=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    image = models.ImageField(upload_to='tickets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate a unique fault code if not provided
        if not self.fault_code:
            date_str = timezone.now().strftime('%y%m%d')
            random_str = str(uuid.uuid4()).split('-')[0][:4].upper()
            self.fault_code = f"FC{date_str}{random_str}"
            
            # Update machine status to fault when ticket is created
            if not self.pk:  # Only on creation
                self.machine.status = 'fault'
                self.machine.update_text = 'Fault Reported'
                self.machine.save()
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.fault_code} - {self.machine.name}"

class TicketUpdate(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_text = models.TextField()
    image = models.ImageField(upload_to='ticket_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Update on {self.ticket.fault_code} by {self.user.first_name}"

class TechnicianAssignment(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'technician'}, related_name='assigned_machines')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='assigned_technicians')
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='assignments/', blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_created')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('technician', 'machine')
    
    def __str__(self):
        return f"{self.machine.name} assigned to {self.technician.first_name}"

class MachineWarning(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='warnings')
    warning_text = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='warnings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Update machine status to warning when a warning is added
        if not self.pk:  # Only on creation
            self.machine.status = 'warning'
            self.machine.warning_text = self.warning_text[:255]
            self.machine.save()
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Warning for {self.machine.name}: {self.warning_text[:30]}"