from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	# Dropbox
	url(r'webhook/$', views.webhook, name= 'rocklistener-webhook'),
)
