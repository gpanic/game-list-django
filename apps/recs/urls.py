from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.recs.models import UserRec

urlpatterns = patterns('apps.recs.views',
	url(r'^$',
		ListView.as_view(
			queryset=UserRec.objects.order_by('-date_created'),
			template_name='recs/userrec_index.html',
		),
		name='recs_userrec_index',
	),
	url(r'^(?P<userrec_id>\d+)/$',
		DetailView.as_view(
			model=UserRec,
			template_name='recs/userrec_details.html',
			pk_url_kwarg='userrec_id',
		),
		name='recs_userrec_details',
	),
	url(r'^add/$', 'userrec_create', name='recs_userrec_create'),
	url(r'^(?P<userrec_id>\d+)/edit/$', 'userrec_update', name='recs_userrec_update'),
	url(r'^(?P<userrec_id>\d+)/delete/$', 'userrec_delete', name='recs_userrec_delete'),
)