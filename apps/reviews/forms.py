from django import forms
from django.forms import Textarea
from apps.reviews.models import Review

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		exclude = (
			'author'
		)
		widgets = {
			'content': Textarea(attrs={'class': 'span6', 'rows': 10})
		}
