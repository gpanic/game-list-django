from django.contrib import admin
from apps.lists.models import List, ListItem
from django.forms import Textarea, TextInput
from django.db import models

class ListItemInline(admin.TabularInline):
	formfield_overrides = {
		models.TextField: {'widget': TextInput},
	}
	model = ListItem
	extra = 1

class ListAdmin(admin.ModelAdmin):
	readonly_fields = [ 'user', ]
	inlines= [
		ListItemInline,
	]

admin.site.register(List, ListAdmin)
admin.site.register(ListItem)