from django import forms
from django.forms import Textarea

from apps.auth.models import GENDER

class UserUpdateForm(forms.Form):
	email = forms.EmailField(max_length=75)
	gravatar_email = forms.EmailField(max_length=75)
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	location = forms.CharField(max_length=100, required=False)
	gender = forms.ChoiceField(choices=GENDER, required=False)
	birthday = forms.DateField(required=False)
	website = forms.CharField(max_length=100, required=False)
	about = forms.CharField(required=False)

	class Meta:
		widgets = {
			'about': Textarea
		}