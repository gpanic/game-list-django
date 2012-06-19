from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.games.models import Genre, Platform, Publisher, Developer, Tag, Game

urlpatterns = patterns('',
	url(r'^$',
		ListView.as_view(
			queryset=Game.objects.all(),
			template_name='games/game_index.html'),
		name='games_game_index',
	),
	url(r'^(?P<game_id>\d+)/$', 'apps.games.views.game_details', name='games_game_details'),
)