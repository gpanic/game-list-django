from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext

def home_index(request):
	return redirect(reverse('games_game_index'), context_instance=RequestContext(request))