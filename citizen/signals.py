from django.db.models.signals import post_save
from .models import Citizen, User

def citizen_profile(sender, instance, created, **kwargs):
	if created:
		Citizen.objects.create(
			citizen=instance,
			)
		print('Profile created!')

post_save.connect(citizen_profile, sender=User)