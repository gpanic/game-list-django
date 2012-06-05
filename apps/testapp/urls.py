from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from apps.testapp.models import Poll

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='testapp/index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll,
            template_name='testapp/detail.html')),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='testapp/results.html'),
        name='poll_results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'apps.testapp.views.vote'),
)