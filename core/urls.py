from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('manager/', views.manager, name='manager'),
    path('assgin-tech/', views.assign_tech, name='assgin-tech'),
    path('raise-ticket/', views.raise_ticket, name='raise-ticket'),

]
