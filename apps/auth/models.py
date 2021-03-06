from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from pybb.models import PybbProfile

from hashlib import md5

GENDER = (
	(0, 'Not given'),
	(1, 'Male'),
	(2, 'Female'),
)

class UserProfile(PybbProfile):
	user = models.OneToOneField(User)

	gravatar_email = models.EmailField(max_length=100)
	location = models.CharField(max_length=100, blank=True)
	gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, default=0)
	birthday = models.DateField(null=True, blank=True)
	website = models.URLField(max_length=100, blank=True)
	about = models.TextField(blank=True)

	def get_gravatar_url(self):
		return "http://www.gravatar.com/avatar/" + md5(self.user.email.strip().lower()).hexdigest() + '?s=80'

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance,gravatar_email=instance.email)

post_save.connect(create_user_profile, sender=User)