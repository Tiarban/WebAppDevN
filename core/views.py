from django.shortcuts import render

def index(request): return render(request, 'core/navbar.html')
def homepage(request): return render(request, 'core/homepage.html')
def manager(request): return render(request, 'core/manager.html')
def technician(request): return render(request, 'core/technician.html')
def machinedetails(request): return render(request, 'core/machinedetails.html')
def assign_tech(request): return render(request, 'core/assign-tech.html')
def raise_ticket(request): return render(request, 'core/raise-ticket.html')
def addwarning(request): return render(request, 'core/addwarning.html')
def machine_detail(request, machine_id): return render(request, 'core/machinedetails.html', {'id': machine_id})




