from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sessions.models import Session
from django.conf import settings
# from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

class UserManager(BaseUserManager):
	def create_user(self, uid, name, email, phone, state, password=None, active=True, staff=False, admin=False):
		if not name:
			raise ValueError('Please provide your Full Name')
		if not password:
			raise ValueError('Please fill in your Password')
		if not email:
			raise ValueError('Please provide a valid Email')
		if not phone:
			raise ValueError('Please provide a valid Mobile Number')
		if not state:
			raise ValueError('which state you belong to')
		if not uid:
			raise ValueError('Please provide your UID')

		user_obj = self.model(
			uid = uid,
			name = name,
			email = self.normalize_email(email),
			phone = phone,
			state = state,
		)
		user_obj.set_password(password)
		user_obj.is_staff = staff
		user_obj.is_admin = admin
		user_obj.is_active = active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, uid, name, email, phone, state, password=None):
		user = self.create_user(
			uid,
			name,
			email,
			phone,
			state,
			password=password,
			staff = True,
		)
		return user
	def create_superuser(self, uid, name, email, phone, state, password=None):
		user = self.create_user(
			uid,
			name,
			email,
			phone,
			state,
			password=password,
			staff = True,
			admin=True,
		)
		return user

class User(AbstractBaseUser):
	uid = models.CharField(max_length=12, unique=True)
	USERNAME_FIELD = 'uid' # username
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False) # staff
	is_admin = models.BooleanField(default=False) # super user
	
	email = models.EmailField(max_length=50)
	name = models.CharField(max_length=50, null=True)
	phone = models.CharField(max_length=10, null=True)
	state = models.CharField(max_length=50, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	# USERNAME_FIELD and password are by default required
	REQUIRED_FIELDS = ['name', 'email', 'phone', 'state']
	objects = UserManager()

	def get_full_name(self):
		self.name
	def get_short_name(self):
		self.name

	def __str__(self):
		return self.uid


	def has_perm(self, perm, obj=None):
		# "Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		# "Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)


class Citizen(models.Model):
	citizen = models.OneToOneField(User, on_delete= models.CASCADE)
	# extra data
	district = models.CharField(max_length=50, null=True)
	dob = models.DateTimeField(max_length=8, null=True)
	age = models.CharField(max_length=3, null=True)
	profile_pic = models.ImageField(default='Koala.jpg', null=True, blank=True)
	# againsts
	against_compliants = models.IntegerField(default=0)
	against_challans = models.IntegerField(default=0)

	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
	)
	gender = models.CharField(max_length=10, null=True, choices=GENDER)
	

	def __str__(self):
		return self.citizen.name

class Appointment(models.Model):
	citizen = models.ForeignKey(Citizen, null=True, on_delete= models.CASCADE)
	description = models.CharField(max_length=1000, null=True)
	WHOM = (
			('DGP', 'DGP'),
			('ADGP', 'ADGP'),
			('IGP', 'IGP'),
			('DIGP', 'DIGP'),
			('SP', 'SP'),
		)
	date_created = date_created = models.DateTimeField(auto_now_add=True, null=True)
	whom = models.CharField(max_length=10, null=True, choices=WHOM)
	status = models.CharField(max_length=50, default="Pending")

	def __str__(self):
		return str(self.citizen)

class Noc(models.Model):
	citizen = models.ForeignKey(Citizen, null=True, on_delete= models.CASCADE)
	NEED = (

			('NOC for Employment', 'NOC for Employment'),
			('NOC for Immigration', 'NOC for Immigration'),
			('NOC for Student', 'NOC for Student'),
	   ) 
	date_created  = models.DateTimeField(auto_now_add=True, null=True)
	need = models.CharField(max_length=30, null=True, choices=NEED)
	status = models.CharField(max_length=50, default="Pending")
	def __str__(self):
		return str(self.citizen)
		
class Compliant(models.Model):
 
	citizen = models.ForeignKey(Citizen, null=True, on_delete= models.CASCADE)
	date_created = date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=50, default="Pending")
	description = models.CharField(max_length=1000, null=True)
	district = models.CharField(max_length=50)
	place = models.CharField(max_length=50)
	CATEGORIES = (
		('Cognizable', 'Cognizable'),
		('Non Cognizable', 'Non Cognizable'),
		('Missing Report', 'Missing Case'),
		('Theft Report', 'Theft Case'),
	)
	category = models.CharField(max_length=50, null=True, choices=CATEGORIES)
	screenshot = models.ImageField(upload_to = 'screenshots/', null=True, blank=True)
	def __str__(self):
		return str(self.citizen)






