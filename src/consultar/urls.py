# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from consultar.views import cons_pltr,cons_dado_levant, meto_query,loca_query,grup_query,consinicial,forcsv
urlpatterns = patterns('',
	url (r'^consulta/(?P<empree>\w+)/$', consinicial, name='consinicial'),
	url (r'^(?P<empree>\w+)/plano_trabalho/$', cons_pltr, name='cons_pltr'),
	url (r'^(?P<empree>\w+)/dados_levanta/$', cons_dado_levant, name='dados_levant'),
	#url (r'^campanha/$', meto_query2, name='meto_query2'),
	url (r'^(?P<empree>\w+)/por_metodo/', meto_query, name='meto_query'),
	url (r'^(?P<empree>\w+)/por_localidade/$', loca_query, name='loca_query'),
	url (r'^(?P<empree>\w+)/por_grupo/$', grup_query, name='grup_query'),
	url (r'^(?P<nomecsv>\w+)$', forcsv, name='forcsv2'),
	url (r'^(?P<nomecsv>\w+)/(?P<codcabeca>\w+)$', forcsv, name='forcsv1'),
	url (r'^(?P<nomecsv>\w+)$', forcsv, name='forcsv'),
	)
