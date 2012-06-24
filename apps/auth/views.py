from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import user_passes_test
from django.forms.util import ErrorList
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from apps.auth.forms import LoginForm
from apps.auth.forms import RegistrationForm
from apps.auth.models import UserProfile

def register(request):
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = RegistrationForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				password_repeat = form.cleaned_data['password_repeat']
				email = form.cleaned_data['email']
				if password == password_repeat:
					if User.objects.filter(username=username).exists():
						form._errors['username'] = ErrorList([u'Username already exists.'])
					else:
						user = User.objects.create_user(username, email, password)
						user.get_profile().gravatar = email
						user.save()
						return redirect(reverse('home_index'), context_instance=RequestContext(request))
				else:
					messages.error(request, 'Passwords do not match.')
		else:
			form = RegistrationForm()
	else:
		return redirect(reverse('home_index'), context_instance=RequestContext(request))

	return render_to_response(
		'auth/register.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

def login(request):
	if not request.user.is_authenticated():
		if request.method =='POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user != None:
					if user.is_active:
						django_login(request, user)
						if request.POST.get('next', 'None') == 'None':
							return redirect(reverse('home_index'), context_instance=RequestContext(request))
						else:
							return redirect(request.POST.get('next'), context_instance=RequestContext(request))
					else:
						messages.error(request, 'Your account has been disabled.')
				else:
					messages.error(request, 'Your username and password were incorrect.')
		else:
			form = LoginForm()
	else:
		return redirect(reverse('home_index'), context_instance=RequestContext(request))
	return render_to_response(
		'auth/login.html',
		{'form': form, 'next':request.GET.get('next', 'None')},
		context_instance=RequestContext(request)
	)

def logout(request):
	django_logout(request)
	return redirect(reverse('home_index'), context_instance=RequestContext(request))