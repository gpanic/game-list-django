from django.shortcuts import render_to_response
from apps.auth.models import RegistrationForm
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.forms.util import ErrorList

def register(request):
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
				user = User.objects.create_user(username, email, password)
				user.save()
				return redirect('/', context_instance=RequestContext(request))
			else:
				form._errors['password_repeat'] = ErrorList([u'Passwords do not match.'])

				
	else:
		form = RegistrationForm()

	return render_to_response('auth/register.html', {'form': form},
		context_instance=RequestContext(request)
	)