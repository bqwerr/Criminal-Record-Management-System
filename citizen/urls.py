from django.urls import path
from  . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="citizen_home"),
    path('compliant/', views.compliant_registration, name="compliant"), 
    path('noc/', views.NOC, name="noc"),
    path('appointment/', views.appointment, name="appointment"),
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='citizen/password_reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='citizen/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='citizen/password_reset_form.html'), name='password_reset_confirm'),
    path('reset-completed/', auth_views.PasswordResetCompleteView.as_view(template_name='citizen/password_reset_completed.html'), name='password_reset_complete'),
]
