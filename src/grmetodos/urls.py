# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import escolheform, del_obj, variaveis, montplacamp,montamet,estac_compl, mostraestacao,defineestacao, gerenciaestacao
from forms import *
from dados.forms import *

urlpatterns = patterns('',
	url (r'^empresa-novo/', escolheform, {'form1':EmpresasForm}, name='empresa'),
	url (r'^novo-plano/(?P<empree>\w+)/', escolheform, {'form1':MetodosadmForm}, name='pltr'),
	url (r'^monta-plano/(?P<empree>\w+)/', montamet, name='montapltr'),
	url (r'^apagar-plano/(?P<empree>\w+)/', escolheform, {'form1':'apagar'}, name='apgpltr'),
	url (r'^del/(\d+)/deletado/$',del_obj, {'model1':MontaEstaEspas},name='del_objespa'),
 	url (r'^del/(\d+)/deletadot/$',del_obj, {'model1':MontaEstaTemps},name='del_objtemp'),
	url (r'^del/(\d+)/deletado_metodo/$',del_obj, {'model1':MetoEmprs},name='del_objmet'),
	url (r'^del/(\d+)/deletada_estacao/$',del_obj, {'model1':MetoEstas},name='del_objesta'),
	url (r'^var_biodivEvar_esfor/(?P<empree>\w+)/', variaveis, name='variaveis'),
	url (r'^planilhas_var_biodivEvar_esfor/(?P<empree>\w+)/', montplacamp, name='montplacamp'),
	url (r'^estacao/(\d+)/', mostraestacao, name='mostraestacao'),
	url (r'^cria_estacao/(?P<empree>\w+)/(?:(?P<metogrup>\d+)?/)(?:(?P<metoesta_eeid>[^/]+)?/)(?:(?P<metoesta_ref>[^/]+)?/)$', gerenciaestacao, name='gerenciaestacao'),
	url (r'^define_estacao/(?P<empree>\w+)/(?P<metogrup>\d+)/$', defineestacao, name='defineestacao'),
	url (r'^estacao_completa/(?P<empree>\w+)/(?P<metogrup>\d+)/$', estac_compl, name='estac_compl'),
)
