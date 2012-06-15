from django import forms

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=128)
	password_repeat = forms.CharField(max_length=128)
	email = forms.EmailField(max_length=75)

	# Details
	# first_name = forms.CharField(max_length=30)
	# last_name = forms.CharField(max_length=30)

	# UserProfile
	# location = forms.CharField(max_length=100)
	# gender = forms.CharField(max_length=6, choices=GENDER, blank=True)
	# birthday = forms.DateField(blank=True)
	# website = forms.CharField(max_length=100, blank=True)
	# about = forms.TextField(blank=True)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=128)