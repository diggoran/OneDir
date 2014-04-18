from django.conf.urls import patterns, url
from onedir import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'))
