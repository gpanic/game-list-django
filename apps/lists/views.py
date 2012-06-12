from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from apps.lists.models import List, ListItem
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
		user = get_object_or_404(User, username=username)
		user.list.listitem_set.add(list_item)
		user.save()
	else:
		raise Http404
	return redirect('apps.lists.views.details', username=username)

@login_required
def remove(request, username, id_game):
	if request.user.username == username:
		game = get_object_or_404(Game, pk=id_game)
		user = get_object_or_404(User, username=username)
		list_item = user.list.listitem_set.get(game=game)
		list_item.delete()
	else:
		raise Http404
	return redirect('apps.lists.views.details', username=username)