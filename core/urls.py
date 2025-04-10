# core/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Manager URLs
    path('manager/', views.manager_dashboard, name='manager'),
    path('assign-tech/', views.assign_technician, name='assign-tech'),
    path('generate-report/', views.generate_report, name='generate-report'),
    
    # Machine management URLs
    path('add-machine/', views.add_machine, name='add-machine'),
    path('machine/<int:machine_id>/edit/', views.edit_machine, name='edit-machine'),
    
    
    # Technician URLs
    path('technician/', views.technician_dashboard, name='technician'),
    
    # Shared URLs
    path('machine/<int:machine_id>/', views.machine_detail, name='machine-detail'),
    path('raise-ticket/', views.raise_ticket, name='raise-ticket'),
    path('add-warning/<int:machine_id>/', views.add_warning, name='add-warning'),
    path('update-ticket/<int:ticket_id>/', views.update_ticket, name='update-ticket'),
    path('about/', views.about_us, name='about'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),



]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)