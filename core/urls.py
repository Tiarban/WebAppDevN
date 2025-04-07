# urls.py - Main URL configuration

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('manager/', views.manager_dashboard, name='manager'),
    path('machine/<int:machine_id>/', views.machine_detail, name='machine-detail'),
    path('assign-tech/', views.assign_tech, name='assign-tech'),
    path('raise-ticket/', views.raise_ticket, name='raise-ticket'),
    path('technician/', views.technician_dashboard, name='technician'),
    path('login/', views.login_view, name='login'),

]

# Add static and media URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)