from django import forms
from django.forms import Textarea
from apps.lists.models import ListItem

class ListItemForm(forms.ModelForm):
	class Meta:
		model = ListItem
		exclude = (
			'game_list',
			'game',
		)
		widgets = {
			'notes': Textarea(attrs={'class': 'input-xlarge', 'rows': 3}),
		}