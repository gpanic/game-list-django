from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.search.views',
	url(r'^$', 'search_redirect', name='search_redirect'),
	url(r'^(?P<search_query>.+)$', 'search_results', name='search_results'),
)