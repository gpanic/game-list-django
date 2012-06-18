from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.games.models import Game
from apps.recs.forms import UserRecForm
from apps.recs.models import UserRec

@login_required
def userrec_create(request):
	if request.method == 'POST':
		form = UserRecForm(request.POST)
		if form.is_valid():
			game1 = form.cleaned_data['game1']
			game2 = form.cleaned_data['game2']
			if game1 != game2:
				game1_set = []
				game2_set = []
				userrec_set = request.user.userrec_set.all()
				for userrec in userrec_set:
					game1_set.append(userrec.game1)
					game2_set.append(userrec.game2)
				if not ((game1 in game1_set and game2 in game2_set) or (game1 in game2_set and game2 in game1_set)):
					form.save()
					return redirect('home_index', context_instance=RequestContext(request))
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