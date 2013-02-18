# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from views import logar,outlog


urlpatterns = patterns('',
#	url(r'^register/$',registrar,name='registrar'),
	url(r'^logar/$',logar,name='logar'),
	url(r'^outlog/$',outlog,name='outlog'),
	
)
