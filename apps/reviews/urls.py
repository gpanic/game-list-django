from django.conf.urls import patterns, include, url
from django.views.generic import ListView

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review

urlpatterns = patterns('apps.reviews.views',
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.all(),
			template_name='reviews/index.html'
		),
		name='reviews.index'
	),
	url(r'^add/$', 'add'),
)