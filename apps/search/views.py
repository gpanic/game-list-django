from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.games.models import Game, Company

def search_redirect(request):
	if request.method == 'POST':
		search_query = request.POST['search_query']
		if  search_query:
			return redirect(reverse('search_results', args=[search_query]), context_instance=RequestContext(request))
	return render_to_response('search/search_results.html', context_instance=RequestContext(request))

def search_results(request, search_query):
	search_query_modified = ''.join(search_query.split()).lower()

	games = Game.objects.all()
	result_games = []
	for game in games:
		if search_query_modified in ''.join(game.title.split()).lower():
			result_games.append(game)

	companies = Company.objects.all()
	result_companies = []
	for company in companies:
		if search_query_modified in ''.join(company.name.split()).lower():
			result_companies.append(company)

	users = User.objects.filter(is_active=True)
	result_users = []
	for user in users:
		if search_query_modified in ''.join(user.username.split()).lower():
			result_users.append(user)

	return render_to_response(
		'search/search_results.html',
		{
			'search_query': search_query,
			'result_games': result_games,
			'result_companies': result_companies,
			'result_users': result_users,
		},
		context_instance=RequestContext(request)
	)