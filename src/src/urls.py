# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	(r'^$', TemplateView.as_view(template_name='index.html')),
	(r'^dados/', include('dados.urls', namespace='dados')),
	(r'^gerencia/', include('gerencia.urls', namespace='gerencia')),
	(r'^novo/',include('usuarios.urls', namespace='usuarios')),
	(r'^consultar/', include('consultar.urls', namespace='consultar')),
	(r'^metodologia/', include('grmetodos.urls', namespace='grmetodos')),

	# Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	#(r'^define_empree/', include('administra.urls', namespace='administra')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
