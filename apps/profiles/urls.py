from django.conf.urls import patterns, include, url
from django.views.generic import DetailView
from django.contrib.auth.models import User

urlpatterns = patterns('',
	url(r'^(?P<username>\w+)/$', 'apps.profiles.views.user_details', name='profiles_user_details'),
	url(r'^(?P<username>\w+)/edit/$', 'apps.profiles.views.user_update', name='profiles_user_update'),
	url(r'^(?P<username>\w+)/reviews/$', 'apps.reviews.views.review_index_for_user', name='reviews_review_index_for_user'),
	url(r'^(?P<username>\w+)/recommendations/$', 'apps.recs.views.userrec_index_for_user', name='recs_userrec_index_for_user'),
	url(r'^(?P<username>\w+)/recommended/$', 'apps.profiles.views.recommended_index', name='profiles_recommended_index'),
	url(r'^(?P<username>\w+)/list/$', 'apps.lists.views.list_details', name='lists_list_details'),
	url(r'^(?P<username>\w+)/list/add/(?P<id_game>\d+)/$', 'apps.lists.views.listitem_create', name='lists_listitem_create'),
	url(r'^(?P<username>\w+)/list/(?P<id_game>\d+)/edit/$', 'apps.lists.views.listitem_update', name='lists_listitem_update'),
	url(r'^(?P<username>\w+)/list/(?P<id_game>\d+)/remove/$', 'apps.lists.views.listitem_delete', name='lists_listitem_delete'),
)