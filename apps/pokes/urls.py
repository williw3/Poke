from django.conf.urls import url
from . import views
urlpatterns=[
	url(r'^$', views.index),
	url(r'^pokes$', views.pokes),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^(?P<id>\d+)$', views.add_poke)
]