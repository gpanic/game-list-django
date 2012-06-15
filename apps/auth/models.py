from django.db import models
from django.contrib.auth.models import User

GENDER = (
	(0, 'Not given'),
	(1, 'Male'),
	(2, 'Female'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	location = models.CharField(max_length=100, blank=True)
	gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, default=0)
	birthday = models.DateField(null=True, blank=True)
	website = models.CharField(max_length=100, blank=True)
	about = models.TextField(blank=True)

