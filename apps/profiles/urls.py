from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^(?P<username>\w+)/reviews$', 'apps.reviews.views.index_for_user'),
	url(r'^(?P<username>\w+)/list$', 'apps.lists.views.details'),
	url(r'^(?P<username>\w+)/list/add/(?P<id_game>\d+)/$', 'apps.lists.views.create'),
	url(r'^(?P<username>\w+)/list/(?P<id_game>\d+)/remove/$', 'apps.lists.views.delete'),
	url(r'^(?P<username>\w+)/list/(?P<id_game>\d+)/edit/$', 'apps.lists.views.update'),
)