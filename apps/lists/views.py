from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.games.models import Game
from apps.lists.forms import ListItemForm
from apps.lists.models import List, ListItem

def list_details(request, username):
	user = User.objects.filter(username=username)
	glist = get_object_or_404(List, user=user)
	return render_to_response(
		'lists/list_details.html',
		{ 'list': glist, },
		context_instance=RequestContext(request)
	)

@login_required
def listitem_create(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		list_item = ListItem()
		list_item.game = game
		request.user.list.listitem_set.add(list_item)
		request.user.save()
	else:
		raise Http404
	return redirect(request.META['HTTP_REFERER'], context_instance=RequestContext(request))

@login_required
def listitem_update(request, username, id_game):
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
		'lists/listitem_edit.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

@login_required
def listitem_delete(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		list_item = request.user.list.listitem_set.get(game=game)
		list_item.delete()
	else:
		raise Http404
	return redirect(request.META['HTTP_REFERER'], context_instance=RequestContext(request))