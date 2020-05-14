from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import RegisterForm, CitizenProfileFormPrimary, CitizenProfileFormSecondary
from django.contrib.auth import get_user_model
from django.contrib import messages
from police.decorators import authenticated_user, citizen_only
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
# Create your views here.


@authenticated_user
def register(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		# print('validating')
		if form.is_valid():
			user = form.save()
			# print('validated')
			username = form.cleaned_data.get('name')
			# group = Group.objects.get(name='customers') # ---------------
			# user.groups.add(group) # ---------------------------
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')

	context = {'form' : form}
	return render(request, 'citizen/register.html', context)

@authenticated_user
def loginView(request):
	if request.method == "POST":
		username = request.POST.get('uid')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user.is_admin:
				return redirect('police_home')
			else:
				return redirect('citizen_home')
		else:
			messages.info(request, 'Username or Password is incorrect')
			return render(request, 'citizen/login.html')
	context = {}
	return render(request, 'citizen/login.html', context)


def logoutView(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@citizen_only
def home(request):
	user = request.user
	# citizen = Citizen.objects.first()
	length = user.citizen.compliant_set.filter(status='Pending').count() + user.citizen.appointment_set.filter(status='Pending').count() + user.citizen.noc_set.filter(status='Pending').count()
	context = {"home_page" : "active", 'user' : user, 'length' : length}
	return render(request, 'citizen/home.html', context)

@login_required(login_url='login')
@citizen_only
def appointment(request):
	user = request.user
	if request.method == "POST":
		description = request.POST.get('description')
		whom = request.POST.get('whom')
		citizen_id = user.citizen.id
		citizen_obj = Citizen.objects.get(id=citizen_id)
		appointment = Appointment(citizen=citizen_obj, description=description, whom=whom, status="Pending")
		appointment.save()
		return redirect('/')
	idx = user.name.find(" ")
	fname = user.name[:idx]
	lname = user.name[idx+1:]
	context = {"appointment_page" : "active", 'fname' : fname, 'lname' : lname}
	return render(request, 'citizen/appointment.html', context)

@login_required(login_url='login')
@citizen_only
def compliant_registration(request):
	user = request.user
	if request.method == "POST":
		description = request.POST.get('description')
		typee = request.POST.get('typee')
		district = request.POST.get('district')
		place = request.POST.get('place')
		approve = request.POST.get('approve')
		citizen_id = user.citizen.id
		citizen_obj = Citizen.objects.get(id=citizen_id)
		compliant = Compliant(citizen=citizen_obj,  status="Pending", description=description, district=district, place=place, category=typee)
		compliant.save()
		return redirect('/')
	idx = user.name.find(" ")
	fname = user.name[:idx]
	lname = user.name[idx+1:]
	context = {"compliant_page" : "active", 'fname' : fname, 'lname' : lname}
	return render(request, 'citizen/compliant.html', context)

@login_required(login_url='login')
@citizen_only
def NOC(request):
	user = request.user
	if request.method == "POST":
		need = request.POST.get('need')
		citizen_id = user.citizen.id
		citizen_obj = Citizen.objects.get(id=citizen_id)
		noc = Noc(citizen=citizen_obj, need=need, status="Pending")
		print(noc.citizen, noc.need, noc.status)
		#article.author = request.user.author # you can check here whether user is related any author
		noc.save()
		return redirect('/')
	context = {"noc_page" : "active", 'user' : user}
	return render(request, 'citizen/noc.html', context)

@login_required(login_url='login')
@citizen_only
def check_status(request):
	pass

@login_required(login_url='login')
@citizen_only
def profile(request):
	user = request.user
	citizen = user.citizen
	form1 = CitizenProfileFormPrimary(instance=user)
	form2 = CitizenProfileFormSecondary(instance=citizen)
	if request.method == 'POST':
		form2 = CitizenProfileFormSecondary(request.POST, request.FILES, instance=citizen)
		if form2.is_valid():
			form2.save()

	context = {'form1' : form1, 'form2' : form2, 'citizen' : citizen}
	return render(request, 'citizen/account_settings.html', context)

@login_required(login_url='login')
@citizen_only
def announcements(request):
	pass



