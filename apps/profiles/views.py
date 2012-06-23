from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from hashlib import md5

from apps.profiles.forms import UserUpdateForm

def user_details(request, username):
	user = User.objects.get(username=username)

	reviews = user.review_set.order_by('-date_created')[:5]
	userrecs = user.userrec_set.order_by('-date_created')[:5]
	gravatar_url = "http://www.gravatar.com/avatar/" + md5(user.email.lower()).hexdigest() + '?s=150'

	return render_to_response(
		'profiles/user_details.html',
		{ 
			'user_profile': user,
			'reviews': reviews,
			'userrecs': userrecs,
			'gravatar_url': gravatar_url,
		},
		context_instance=RequestContext(request)
	)

@login_required
def user_update(request, username):
	if request.user.username == username:
		user = request.user
		if request.method == 'POST':
			form = UserUpdateForm(request.POST)
			if form.is_valid():
				user.email = form.data['email']
				user.first_name = form.data['first_name']
				user.last_name = form.data['last_name']
				user.get_profile().location = form.data['location']
				user.get_profile().gender = form.data['gender']
				user.get_profile().birthday = form.data['birthday']
				user.get_profile().website = form.data['website']
				user.get_profile().about = form.data['about']

				user.get_profile().save()
				user.save()
				messages.success(request, 'Your profile has been sucessfully updated.')
		else:
			initial = {
				'email': user.email,
				'first_name': user.first_name,
				'last_name': user.last_name,
				'location': user.get_profile().location,
				'gender': user.get_profile().gender,
				'birthday': user.get_profile().birthday,
				'website': user.get_profile().website,
				'about': user.get_profile().about,
			}
			form = UserUpdateForm(initial=initial)
	else:
		raise Http404

	return render_to_response(
		'profiles/user_edit.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)