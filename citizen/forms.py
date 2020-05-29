# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
# from .views import current_site
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text,DjangoUnicodeDecodeError
from .utils import generate_token

import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

class UserSaveThread(threading.Thread):
    def __init__(self, user):
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        self.user.save()
        email_subject = 'Account Activation'
        message = render_to_string('citizen/activate.html',
                {
                    'user' : self.user,
                    'domain' : settings.ALLOWED_HOSTS[0],
                    'uid' : urlsafe_base64_encode(force_bytes(self.user.id)),
                    'token' : generate_token.make_token(self.user)
                }
            )

        email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [self.user.email]
            )
        # email_message.send()
        EmailThread(email_message).start()

        

class LoginForm(forms.Form):
    uid = forms.CharField(label='UID', max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
        
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # email = VerifiedEmailField(label='email', required=True)
    class Meta:
        model = User
        fields = ('uid','name', 'email', 'phone', 'state')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone=phone)
        if len(str(phone)) < 10 or not str(phone).isdigit():
            raise forms.ValidationError("Enter Valid Mobile Number")
        if qs.exists():
            raise forms.ValidationError("Mobile Number is already Registered")
        return phone

    def clean_uid(self):
        uid = self.cleaned_data.get('uid')
        us = User.objects.filter(uid=uid)
        if us.exists():
            raise forms.ValidationError('Enter valid UID')
        return uid

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            UserSaveThread(user).start()

        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('uid','name', 'email', 'phone', 'state')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.

    password = ReadOnlyPasswordHashField()
    """
    
    password = ReadOnlyPasswordHashField(label=("Password"),help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                      "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# profile
class CitizenProfileFormPrimary(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uid', 'name', 'phone', 'email', 'state',]
        exclude = ['password', 'last_login', 'is_active', 'is_staff', 'is_admin']

class CitizenProfileFormSecondary(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = '__all__'
        exclude = ['citizen', 'against_compliants', 'against_challans']