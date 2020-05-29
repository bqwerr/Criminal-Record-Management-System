from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import RegisterForm, CitizenProfileFormPrimary, CitizenProfileFormSecondary
from django.contrib.auth import get_user_model
from django.contrib import messages
from police.decorators import authenticated_user, citizen_only
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import generate_token
from django.utils.encoding import force_bytes, force_text,DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
import os
import glob


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
			messages.success(request, 'Account has been created for ' + username +', Please Verify your E-mail to Login')
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
				messages.success(request, 'Hi ' + request.user.name + ',  Welcome to CityDesk-Police Panel. You can now handle Services Online!!')
				return redirect('police_home')
			else:
				messages.success(request, 'Hi ' + request.user.name + ',  Welcome to CityDesk-Citizen Panel' + ' Explore the services !!')
				return redirect('citizen_home')
		else:
			messages.error(request, 'Username or Password is Incorrect')
			return redirect('login')
	context = {}
	return render(request, 'citizen/login.html', context)


def logoutView(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@citizen_only
def home(request):
	'''
	print(request.session.items()) -> prints session query dict
	print(request.session.get_expiry_age()) -> prints session expiry in secs
	
	To update session expiry time for each request instead of using SESSION_SAVE_EVERY_REQUEST attribute
	print(request.session.set_expiry(request.session.get_expiry_age()))
	'''
	user = request.user
	# citizen = Citizen.objects.first()
	fname = user.name.split(" ")[0]
	length = user.citizen.compliant_set.filter(status='Pending').count() + user.citizen.appointment_set.filter(status='Pending').count() + user.citizen.noc_set.filter(status='Pending').count()
	context = {"home_page" : "active", 'user' : user, 'length' : length, 'fname':fname}
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
		messages.success(request, 'Received your Appointment request, We will Contact you Soon.')
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
		files = request.FILES.getlist('image')
	
		image = None
		if 'image' in request.FILES:
			image = request.FILES['image']
		citizen_id = user.citizen.id
		citizen_obj = Citizen.objects.get(id=citizen_id)
		compliant = Compliant(citizen=citizen_obj,  status="Pending", description=description, district=district, place=place, category=typee, screenshot=image)
		compliant.save()
		messages.success(request, 'Received your Compliant, We will Contact you Soon.')
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
	fname = user.name.split(" ")[0]
	if request.method == "POST":
		need = request.POST.get('need')
		citizen_id = user.citizen.id
		citizen_obj = Citizen.objects.get(id=citizen_id)
		noc = Noc(citizen=citizen_obj, need=need, status="Pending")
		#print(noc.citizen, noc.need, noc.status)
		#article.author = request.user.author # you can check here whether user is related any author
		noc.save()
		messages.success(request, 'Received your NOC request, We will Contact you Soon.')
		return redirect('/')
	context = {"noc_page" : "active", 'user' : user, 'fname' : fname }
	return render(request, 'citizen/noc.html', context)

@login_required(login_url='login')
@citizen_only
def check_status(request):
	pass

@login_required(login_url='login')
@citizen_only
def profile(request):
	user = request.user
	fname = user.name.split(" ")[0]
	citizen = user.citizen
	prev_image_url = None
	if citizen.profile_pic:
		prev_image_url = citizen.profile_pic.url
	form1 = CitizenProfileFormPrimary(instance=user)
	form2 = CitizenProfileFormSecondary(instance=citizen)
	if request.method == 'POST':
		form2 = CitizenProfileFormSecondary(request.POST, request.FILES, instance=citizen)
		if form2.is_valid():
			if citizen.profile_pic and prev_image_url:
				if prev_image_url !=  citizen.profile_pic.url and "Koala" not in prev_image_url:
					file = 'static' + prev_image_url
					os.remove(file)
			form2.save()
			messages.info(request, 'Profile Updated !!')

	context = {'form1' : form1, 'form2' : form2, 'citizen' : citizen, 'fname':fname}
	return render(request, 'citizen/account_settings.html', context)

@login_required(login_url='login')
@citizen_only
def announcements(request):
	pass

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(id=uid)
		
	except Exception as identifier:
		user = None
		print(user)

	if user and generate_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Account activated Successfully')
		return redirect('login')

	return redirect('register')
