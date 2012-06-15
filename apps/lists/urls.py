from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.lists.views',
	url(r'^(?P<username>\w+)/$', 'details'),
	url(r'^(?P<username>\w+)/add/(?P<id_game>\d+)/$', 'add'),
	url(r'^(?P<username>\w+)/remove/(?P<id_game>\d+)/$', 'remove'),
	url(r'^(?P<username>\w+)/edit/(?P<id_game>\d+)/$', 'edit'),
)