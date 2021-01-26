from django.shortcuts import render
from django.http import HttpResponse
from citizen.models import *
from .filters import OrderFilter
from citizen.models import User
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
def view_records(request):
	user = request.user
	users = User.objects.all()
	myFilter = OrderFilter(request.GET, queryset=users)
	users = myFilter.qs
	fname = user.name.split(" ")[0]
	context = {'fname' : fname, 'records_page' : 'active', 'myFilter' : myFilter}
	return render(request, "police/view_records.html", context)

@login_required(login_url='login')
@police_only
def citizen_profile(request, pk, typ):
	user = request.user
	citizen = Citizen.objects.get(id=pk)
	compliants = citizen.compliant_set.order_by('-date_created')[:5]
	nocs = citizen.noc_set.order_by('-date_created')[:5]
	appointments = citizen.appointment_set.order_by('-date_created')[:5]
	fname = user.name.split(" ")[0]
	context = {'fname' : fname, 'citizen' : citizen, 'compliants' : compliants, 'nocs' : nocs, 'appointments' : appointments, 'typ' : int(typ)}
	return render(request, 'police/citizen.html', context)

 
@login_required(login_url='login')
@police_only
def home(request):
	compliants = Compliant.objects.all()
	appointments = Appointment.objects.all()
	nocs = Noc.objects.all()
	fname = request.user.name.split(" ")[0]
	context = {"home_page" : "active", 
	'compliants' : compliants, 
	'appointments' : appointments,
	'nocs'  : nocs,
	'fname' : fname,
	}
	return render(request, "police/home.html", context)

@login_required(login_url='login')
@police_only
def match_face(request):
	return render(request, "police/match.html")



