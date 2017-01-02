from django.conf.urls import url

from . import views

app_name = 'finder'
urlpatterns = [
	# ex: / or /finder/
	url(r'^$', views.IndexView.as_view(), name='index'),
	# ex: /finder/5/
	url(r'^(?P<embassy_id>[0-9]+)/$', views.EmbassyView.as_view(), name='embassy_info'),
	# ex: /finder/ABC/
	url(r'^(?P<code>[A-Z]{3})/$', views.CountryView.as_view(), name='country_info'),
	# ex: /finder/find/ABC/DEF
	url(r'^find/(?P<government_code>[A-Z]{3})/(?P<location_code>[A-Z]{3})/$', views.results, name='results'),
	# ex: /finder/find/ABC/DEF
	url(r'^search/', views.search, name='search'),
]