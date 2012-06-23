from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('apps.home.urls')),
    url(r'^', include('apps.auth.urls')),
    url(r'^', include('apps.games.urls')),
    url(r'^testapp/', include('apps.testapp.urls')),
    url(r'^users/', include('apps.profiles.urls')),
    url(r'^lists/', include('apps.lists.urls')),
    url(r'^reviews/', include('apps.reviews.urls')),
    url(r'^recommendations/', include('apps.recs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'gamelist.views.homegamelistname='home'),
    # url(r'^gamelist/', include('gamelist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)