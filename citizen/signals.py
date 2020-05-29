from django.db.models.signals import post_save
from .models import Citizen, User, UserSession
from django.contrib.sessions.models import Session
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

def citizen_profile(sender, instance, created, **kwargs):
	if created:
		Citizen.objects.create(
			citizen=instance,
			)
		# print('Profile created!')


# The citizen_profile function will only be called when an instance of User is saved.
post_save.connect(citizen_profile, sender=User)


@receiver(user_logged_in) # request started
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()

    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
    )
