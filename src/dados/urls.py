# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from forms import *
from gerencia.forms import DocumentForm
from dados.views import importfolder, succok,uploaddata, retirapop, eraselevant, erasecamp, del_leva, del_camp
from dados.models import Empreendimentos
from dados.forms import Empreendimentos1Form
from gerencia.views import *
urlpatterns = patterns('',
    
	#url(r'^sucesso/$',success,name='success'),
	#url (r'^media/documents/(\d+)/(\d+)/(\d+)/(\w+)/$',verifica, name='verifica'),
	#url (r'^import/', importgeral,{'modd':GradesModulos, 'cab':['nome','empreendimento','tipo','qnt_trilhas'], 'empree':Empreendimentos.objects.get(id=1)}, name='importgeral'),
	#url(r'^list/$', listo, name='listo'),
#	url (r'^erro/$', erroanadois,name='erroanadois'),
	url (r'^upload_data/(?P<empree>\w+)/', uploaddata, name='uploaddata'),
	url (r'^esfor_biodiv_upload$', retirapop,name='retirapop'),
	url (r'^biodiv_esfor_zip_import/(?P<empree>\w+)/', importfolder, name='importfolder'),
#	url (r'^([^/]+)/(\w+)*$', succok,name='succok'),
	url (r'^eraselevant/(?P<empree>\w+)/', eraselevant, name='eraselevant'),
	url (r'^erasecamp/(?P<empree>\w+)/', erasecamp, name='erasecamp'),
	url (r'^sucesso/(?P<empree>\w+)/(?P<lista>[^/]+)/*$', succok,name='succok'),
	url (r'^levantamento/(?P<pk>\d+)/deletado/(?P<empree>\w+)/$',del_leva,name='del_leva'),
	url (r'^campanha/(?P<pk>\d+)/deletado/(?P<empree>\w+)/$',del_camp,name='del_camp'),	
#	url (r'^(?P<empree>\w+)/(?P<lista>.*?)/*$', succok,name='succok'),
	
 #   url (r'^empreendimento-novo/', escolhefrom, {'form1':EmpreendimentosForm}, name='empree'),
#	url (r'^empresa-novo/', putform, {'formin':EmpresasForm}, name='empresa'),
#	url (r'^novo-plano/', putform, {'formin':MetodosadmForm}, name='pltr'),
#	url (r'^(\d+)/deletado/$',del_obj, {'model1':MontaEstaEspas},name='del_objespa'),
 #	url (r'^(\d+)/deletadot/$',del_obj, {'model1':MontaEstaTemps},name='del_objtemp'),
)
