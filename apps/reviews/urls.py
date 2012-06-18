from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review

urlpatterns = patterns('apps.reviews.views',
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.all(),
			template_name='reviews/review_index.html',
		),
		name='reviews_review_index',
	),
	url(r'^add/$', 'review_create', name='reviews_review_create'),
	url(r'^(?P<review_id>\d+)/$',
		DetailView.as_view(
			model=Review,
			template_name='reviews/review_details.html',
			pk_url_kwarg='review_id',
		),
		name='reviews_review_details',
	),
	url(r'^(?P<review_id>\d+)/edit/$', 'review_update', name='reviews_review_update'),
	url(r'^(?P<review_id>\d+)/remove/$', 'review_delete', name='reviews_review_delete'),

)