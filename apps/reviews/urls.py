from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review

urlpatterns = patterns('apps.reviews.views',
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.all(),
			template_name='reviews/index.html',
		),
		name='reviews.index'
	),
	url(r'^add/$', 'add'),
	url(r'^(?P<review_id>\d+)/$',
		DetailView.as_view(
			model=Review,
			template_name='reviews/details.html',
			pk_url_kwarg='review_id',
		),
		name='reviews.details'
	),
	url(r'^(?P<review_id>\d+)/edit/$', 'edit'),
	url(r'^(?P<review_id>\d+)/remove/$', 'remove'),

)