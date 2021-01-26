from django.db import models

from django_base64field.fields import Base64Field

class CrimeRecords(models.Model):
	key = models.CharField(primary_key=True, unique=True, max_length=30)
	name =  models.CharField(max_length=50, null=True)
	against = models.CharField(max_length=5, null=True)
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
	)
	img = Base64Field(max_length=900000, blank=True, null=True)
	gender = models.CharField(max_length=10, null=True, choices=GENDER)
	key_points = models.CharField(max_length=90000, null=True)

	def __str__(self):
		return self.key
   
