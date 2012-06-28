from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
	# url(r'^$',
	# 	TemplateView.as_view(
	# 		template_name='home/index.html'),
	# 	name="home_index"),
	url(r'^$', 'apps.home.views.home_index', name='home_index'),
)