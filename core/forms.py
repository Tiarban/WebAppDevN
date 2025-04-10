# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Machine, Ticket, TicketUpdate, TechnicianAssignment, MachineWarning

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['code', 'name', 'description', 'status', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter machine code e.g., M001'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter machine name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter machine description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['machine', 'title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Issue Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue...', 'rows': 4}),
            'machine': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketUpdateForm(forms.ModelForm):
    STATUS_CHOICES = Ticket.STATUS_CHOICES
    
    ticket_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = TicketUpdate
        fields = ['update_text', 'image']
        widgets = {
            'update_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter update details...', 'rows': 4}),
        }

class TechnicianAssignmentForm(forms.ModelForm):
    class Meta:
        model = TechnicianAssignment
        fields = ['technician', 'machine', 'notes', 'image']
        widgets = {
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'machine': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter notes here...', 'rows': 4}),
        }

class MachineWarningForm(forms.ModelForm):
    class Meta:
        model = MachineWarning
        fields = ['warning_text', 'image']
        widgets = {
            'warning_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter warning details...', 'rows': 4}),
        }
