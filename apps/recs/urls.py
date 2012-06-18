from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.recs.models import UserRec

urlpatterns = patterns('apps.recs.views',
	url(r'^$',
		ListView.as_view(
			queryset=UserRec.objects.all(),
			template_name='recs/userrec_index.html',
		),
		name='recs_userrec_index',
	),
	url(r'^(?P<rec_id>\d+)/$',
		DetailView.as_view(
			model=UserRec,
			template_name='recs/userrec_details.html',
			pk_url_kwarg='rec_id',
		),
		name='recs_userrec_details',
	),
	url(r'^add/$', 'userrec_create', name='recs_userrec_create'),
)