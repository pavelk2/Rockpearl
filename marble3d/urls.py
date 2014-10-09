from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

import views


urlpatterns = patterns('',
    # Home page
	url(r'^$', views.BlockListView.as_view(), name= 'marble3d-home'),
	# Management of blocks and images
	url(r'create/$', login_required(views.BlockCreateView.as_view()), name= 'marble3d-block-create'),
	url(r'blocks/(?P<block_pk>\d+)/$', login_required(views.ImageListView.as_view()), name= 'marble3d-image-list'),
	url(r'blocks/(?P<block_pk>\d+)/update/$', login_required(views.BlockUpdateView.as_view()), name= 'marble3d-block-update'),
	url(r'images/(?P<image_pk>\d+)/update/$', login_required(views.ImageUpdateView.as_view()), name= 'marble3d-image-update'),
	
	url(r'blocks/(?P<block_pk>\d+)/upload/$', login_required(views.uploadImage), name= 'marble3d-image-upload'),
	
	# Endpoints which CrowdCafe calls:
	# --------------------------------------------------------------------------------------
	# Quality control
	url(r'judgements/control/$', views.controlJudgement, name= 'marble3d-judgement-control'),
	# Results webhook
	url(r'judgements/receive/$', views.receiveJudgement, name= 'marble3d-judgement-receive'),
	# --------------------------------------------------------------------------------------
)
