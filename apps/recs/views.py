from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.models import User

from apps.games.models import Game
from apps.recs import rec_engine
from apps.recs.forms import UserRecForm, UserRecUpdateForm
from apps.recs.models import UserRec

@login_required
def userrec_index_for_user(request, username):
	userrec_list = User.objects.get(username=username).userrec_set.all()

	return render_to_response(
		'profiles/userrec_index_for_user.html',
		{ 'userrec_list': userrec_list, },
		context_instance=RequestContext(request)
	)

@login_required
def userrec_create(request):
	if request.method == 'POST':
		userrec = UserRec()
		userrec.author = request.user
		form = UserRecForm(request.POST, instance=userrec)
		if form.is_valid():
			game1 = form.cleaned_data['game1']
			game2 = form.cleaned_data['game2']
			print game1
			print game2
			if game1 != game2:
				game1_set = []
				game2_set = []
				userrec_set = request.user.userrec_set.all()
				print userrec_set
				for userrec in userrec_set:
					game1_set.append(userrec.game1)
					game2_set.append(userrec.game2)
				if  game1 in game1_set and game2 in game2_set:
					print True
				else:
					print False
				if not ((game1 in game1_set and game2 in game2_set) or (game1 in game2_set and game2 in game1_set)):
					form.save()
					return redirect(reverse('recs_userrec_index'), context_instance=RequestContext(request))
				else:
					messages.error(request, 'You already made this recommendation, choose different games.')
			else:
				messages.error(request, 'You can\'t make a recommendation for the same game.')
	else:
		form = UserRecForm()

	return render_to_response(
		'recs/userrec_add.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

@login_required
def userrec_update(request, userrec_id):
	userrec = get_object_or_404(UserRec, pk=userrec_id)
	if request.user == userrec.author:
		if request.method == 'POST':
			form = UserRecUpdateForm(request.POST, instance=userrec)
			if form.is_valid():
				form.save()
				messages.success(request, 'Entry updated.')
		else:
			form = UserRecUpdateForm(instance=userrec)
	else:
		raise Http404

	return render_to_response(
		'recs/userrec_edit.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

@login_required
def userrec_delete(request, userrec_id):
	userrec = get_object_or_404(UserRec, pk=userrec_id)
	if request.user == userrec.author:
		userrec.delete()
	else:
		raise Http404
	return redirect(reverse('recs_userrec_index'), context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_matrix(request):
	rec_engine.create_matrix()
	messages.success(request, 'Matrix created.')
	try:
		return redirect(request.META['HTTP_REFERER'], context_instance=RequestContext(request))
	except KeyError:
		raise Http404

@login_required
@user_passes_test(lambda u: u.is_superuser)
def drop_matrix(request):
	rec_engine.drop_matrix()
	messages.success(request, 'Matrix dropped.')
	try:
		return redirect(request.META['HTTP_REFERER'], context_instance=RequestContext(request))
	except KeyError:
		raise Http404

@login_required
@user_passes_test(lambda u: u.is_superuser)
def populate_matrix(request):
	rec_engine.populate_matrix()
	messages.success(request, 'Matrix populated.')
	try:
		return redirect(request.META['HTTP_REFERER'], context_instance=RequestContext(request))
	except KeyError:
		raise Http404
