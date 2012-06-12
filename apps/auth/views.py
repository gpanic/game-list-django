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

from apps.auth.models import LoginForm
from apps.auth.models import RegistrationForm
from apps.lists.models import List

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
						user.save()
						glist = List(user=user)
						glist.save()
						return redirect('home.index')
				else:
					messages.error(request, 'Passwords do not match.')		
		else:
			form = RegistrationForm()
	else:
		return redirect('home.index')
	return render_to_response(
		'auth/register.html',
		{'form': form},
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
							return redirect('home.index')
						else:
							return redirect(request.POST.get('next', 'None'))
					else:
						messages.error(request, 'Your account has been diabled.')
				else:
					messages.error(request, 'Your username and password were incorrect.')
		else:
			form = LoginForm()
	else:
		return redirect('home.index')
	return render_to_response(
		'auth/login.html',
		{'form': form, 'next':request.GET.get('next', 'None')},
		context_instance=RequestContext(request)
	)

def logout(request):
	django_logout(request)
	return redirect('home.index')