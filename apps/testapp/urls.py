from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from apps.testapp.models import Poll

# Uncomment the next two lines to enable the admin:
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
    # Examples:
    # url(r'^$', 'gamelist.views.home', name='home'),
    # url(r'^gamelist/', include('gamelist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
