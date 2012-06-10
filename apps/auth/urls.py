from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.auth.views',
    url(r'^register$', 'register'),
    url(r'^login$', 'login'),
    url(r'logout$', 'logout'),
)