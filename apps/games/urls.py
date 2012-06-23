from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.games.models import Game, Company

urlpatterns = patterns('',
	url(r'^games/$',
		ListView.as_view(
			queryset=Game.objects.order_by('-release_date'),
			template_name='games/game_index.html',
		),
		name='games_game_index',
	),
	url(r'^games/(?P<game_id>\d+)/$', 'apps.games.views.game_details', name='games_game_details'),
)

urlpatterns += patterns('apps.games.views',
	url(r'^companies/$',
		ListView.as_view(
			queryset=Company.objects.order_by('name'),
			template_name='games/company_index.html',
		),
		name='games_company_index',
	),
	url(r'^companies/(?P<company_id>\d+)/$', 'company_details', name='games_company_details'),
)