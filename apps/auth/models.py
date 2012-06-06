from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	GENDER = (
		('', 'Not given'),
		('male', 'Male'),
		('female', 'Female'),
	)

	location = models.CharField(max_length=100, blank=True)
	gender = models.CharField(max_length=6, choices=GENDER, blank=True)
	birthday = models.DateField(null=True, blank=True)
	website = models.CharField(max_length=100, blank=True)
	about = models.TextField(blank=True)