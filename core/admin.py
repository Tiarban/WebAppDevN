from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Machine, Ticket, TicketUpdate, TechnicianAssignment, MachineWarning

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Machine)
admin.site.register(Ticket)
admin.site.register(TicketUpdate)
admin.site.register(TechnicianAssignment)
admin.site.register(MachineWarning)