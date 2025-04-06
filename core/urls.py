from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='home'),
    path('', views.homepage, name='homepage'),
    path('manager/', views.manager, name='manager'),
    path('machinedetails/', views.machinedetails, name='machinedetails'),
    path('assgin-tech/', views.assign_tech, name='assgin-tech'),
    path('raise-ticket/', views.raise_ticket, name='raise-ticket'),
    path('addwarning/', views.addwarning, name='addwarning'),
    path('machines/<int:machine_id>/', views.machine_detail, name='machine-detail'),
    path('technician/', views.technician, name='technician'),


]
