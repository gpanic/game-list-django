from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from apps.lists.models import List, ListItem, ListItemForm
from apps.games.models import Game

def details(request, username):
	user = User.objects.filter(username=username)
	glist = get_object_or_404(List, user=user)
	return render_to_response('lists/details.html',
		{'list': glist,},
		context_instance=RequestContext(request)
	)

@login_required
def add(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		list_item = ListItem()
		list_item.game = game
		request.user.list.listitem_set.add(list_item)
		request.user.save()
	else:
		raise Http404
	return redirect('apps.lists.views.details', username=username)

@login_required
def remove(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		list_item = request.user.list.listitem_set.get(game=game)
		list_item.delete()
	else:
		raise Http404
	return redirect('apps.lists.views.details', username=username)

@login_required
def edit(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		try:
			list_item = request.user.list.listitem_set.get(game=game)
		except ObjectDoesNotExist:
			raise Http404
		if request.method == 'POST':
			form = ListItemForm(request.POST, instance=list_item)
			if form.is_valid():
				form.save()
				messages.success(request, 'Entry updated.')
		else:
			form = ListItemForm(instance=list_item)
	else:
		raise Http404

	return render_to_response(
		'lists/items/edit.html',
		{ 'form':form, },
		context_instance=RequestContext(request)
	)