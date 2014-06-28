from django.conf.urls import patterns, url, include
from maps import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^place/(?P<place_title_url>[-\w]+)/$', views.place, name='place'),
	url(r'^page/(?P<page_url>\w+)/$', views.page, name='page'),
	url(r'^like_place/$', views.like_place, name='like_place'),
	url(r'^place/single/(?P<place_title_url>[-\w]+)/$', views.single, name='single'),
	url(r'^places/tagged/(?P<tag>\w+)/$', views.tag, name='tag'),
	url(r'^search/', views.search, name='search'),
	)