from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from apps.games.models import Genre, Platform, Publisher, Developer, Tag, Game

urlpatterns = patterns('',
	url(r'^$',
		ListView.as_view(
			queryset=Game.objects.all(),
			template_name='games/index.html'),
		name='games.index'),
	url(r'^(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Game,
			template_name='games/detail.html'),
		name='games.detail'),
)