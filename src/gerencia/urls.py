# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from dados.models import Empreendimentos
from dados.forms import Empreendimentos1Form
from gerencia.views import *
urlpatterns = patterns('',
    
	url(r'^escolhe_empreendimento/$',escolheform,{'formin':Empreendimentos1Form},name='escolheformin'),
	url (r'^novo_empreendimento/$',escolheform,{'formin':EmpreendimentosForm}, name='novoempree'),
	url (r'^sucesso/Empreendimento_(?P<empree>\w+)/$',success,{'strmodd':'empreendimento', 'modd':Empreendimentos}, name='successEmpree'),
	url (r'^solos_import/(?P<empree>\w+)/', importgeral,{'modd':Solos, 'cab':cablocal('solos','cab'),'ca':cablocal('solos','ca')}, name='importsolo'),	
	url (r'^inclinacoes_import/(?P<empree>\w+)/', importgeral,{'modd':Inclinacoes, 'cab':cablocal('inclinacoes','cab'),'ca':cablocal('inclinacoes','ca')}, name='importincl'),	
	url (r'^topografias_import/(?P<empree>\w+)/', importgeral,{'modd':Topografias, 'cab':cablocal('topografias','cab'),'ca':cablocal('topografias','ca')}, name='importtopo'),	
	url (r'^campanhas_import/(?P<empree>\w+)/', importgeral,{'modd':Campanhas, 'cab':cablocal('campanhas','cab'),'ca':cablocal('campanhas','ca')}, name='importcamp'),	
	url (r'^coordenadas_import/(?P<empree>\w+)/', importgeral,{'modd':Coordenadas, 'cab':cablocal('coordenadas','cab'),'ca':cablocal('coordenadas','ca')}, name='importcoor'),	
	url (r'^parcelas_import/(?P<empree>\w+)/', importgeral,{'modd':Parcelas, 'cab':cablocal('parcelas','cab'),'ca':cablocal('parcelas','ca')}, name='importparc'),
	url (r'^trilhas_import/(?P<empree>\w+)/', importgeral,{'modd':Trilhas, 'cab':cablocal('trilhas','cab'),'ca':cablocal('trilhas','ca')}, name='importtril'),
	url (r'^gradesmodulos_import/(?P<empree>\w+)/', importgeral,{'modd':GradesModulos, 'cab':cablocal('gradesmodulos','cab'), 'ca':cablocal('gradesmodulos','ca')}, name='importgrmo'),
	url (r'^consulta/', verdoc, name='verdoc'),
)
