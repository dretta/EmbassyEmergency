from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: / or /finder/
	url(r'^$', views.index, name='index'),
	# ex: /finder/5/
	url(r'^(?P<embassy_id>[0-9]+)/$', views.embassy_info, name='embassy_info'),
	# ex: /finder/ABC/
	url(r'^(?P<code>[A-Z]{3})/$', views.country_info, name='country_info'),
	# ex: /finder/find/ABC/DEF
	url(r'^find/(?P<government>[A-Z]{3})/(?P<location>[A-Z]{3})/$', views.results, name='results'),
]