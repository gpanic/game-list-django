from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

GENDER = (
	(0, 'Not given'),
	(1, 'Male'),
	(2, 'Female'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	gravatar_email = models.EmailField(max_length=100)
	location = models.CharField(max_length=100, blank=True)
	gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, default=0)
	birthday = models.DateField(null=True, blank=True)
	website = models.CharField(max_length=100, blank=True)
	about = models.TextField(blank=True)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)