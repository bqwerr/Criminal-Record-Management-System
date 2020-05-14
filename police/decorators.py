from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		if user.is_authenticated and user.is_admin:
			return redirect('/police/')
		elif user.is_authenticated and user.is_admin==False:
			return redirect('/')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def citizen_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		if user.is_admin:
			return redirect('/police/')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def police_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		if not user.is_admin:
			return redirect('/')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func