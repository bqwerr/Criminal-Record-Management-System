from django.shortcuts import render
from django.http import HttpResponse
from citizen.models import *
from .decorators import authenticated_user, police_only
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@police_only
def accept_appointment(request):
	pass


@login_required(login_url='login')
@police_only
def accept_compliant(request):
	pass

@login_required(login_url='login')
@police_only
def announce_news(request):
	pass
 
@login_required(login_url='login')
@police_only
def home(request):
	compliants = Compliant.objects.all()
	appointments = Appointment.objects.all()
	nocs = Noc.objects.all()
	context = {"home_page" : "active", 
	'compliants' : compliants, 
	'appointments' : appointments,
	'nocs'  : nocs}
	return render(request, "police/home.html", context)
