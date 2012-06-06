from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from apps.auth.models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	fk_name = 'user'
	max_num = 1

class UserProfileAdmin(UserAdmin):
	inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)