from django import forms
from django.forms import Textarea

from apps.recs.models import UserRec

class UserRecForm(forms.ModelForm):
	class Meta:
		model = UserRec
		exclude = (
			'author'
		)
		widgets = {
			'content': Textarea(attrs={'class': 'span6', 'rows': 10})
		}

class UserRecUpdateForm(forms.ModelForm):
	class Meta:
		model = UserRec
		exclude = (
			'author',
			'game1',
			'game2',
		)
		widgets = {
			'content': Textarea(attrs={'class': 'span6', 'rows': 10})
		}