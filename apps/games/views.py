from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from apps.games.models import Game

def game_details(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	game1_set = list(game.userrec_game1.all())
	game2_set = list(game.userrec_game2.all())
	related_userrecs = game1_set + game2_set

	return render_to_response(
		'games/game_details.html',
		{
			'game': game,
			'related_userrecs': related_userrecs,
		},
		context_instance=RequestContext(request)
	)