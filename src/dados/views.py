#-*- coding: utf-8 -*-
from models import *
from forms import *
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from dados.models import Empreendimentos
from models import *
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from gerencia.forms import *
from gerencia.models import *
from zipfile import ZipFile
import zipfile
import os
from django.core.validators import EMPTY_VALUES
from datetime import time, datetime
import glob
from django.db import transaction
import string
import shutil
import random
from django import template
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

cab_lev=[i.name for i in Levantamentos._meta.fields]
cab_ani=[i.name for i in AnimaisDados._meta.fields]
cab_pla=[i.name for i in PlantasDados._meta.fields]
cab_uaa=[i.name for i in UaAvulsas._meta.fields]
dic_tipo_vlr={'1':'Date','2':'Float','3':'Varchar','4':'Integer','5':'Time','6':'Text'}
dic_referencia={'1':'Animais','2':'Plantas','3':'Abioticos'}
dic_tipo_vlr_test={'1':datetime,'2':float,'3':str,'4':int,'5':time,'6':'Text'}


def montadic_zip(doc,ca,metodo,campanha,empree):
	dt1={}
	
	for v,i in enumerate(doc):
		dt1['line%s'%v]=dict(zip(ca,i))
#	empree=Empreendimentos.objects.get(empreendimento=empree)
	try:
		if doc==docesfor:
			for k,v in dt1.iteritems():
				v.update(metodo=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento__empreendimento=empree))
			try:
				for k,v in dt1.iteritems():
					v.update(campanha=Campanhas.objects.get(metodo__metodo__metogrup__metodo__metodo=metodo, empreendimento=empree))
			except: pass
	except: pass
	dt1=alteradt(dt1)
	return dt1
#Metodosp.objects.get(metodo__metodo__iexact=ii[1],empreendimento__empreendimento=empree
#MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=ii[1],metodo__empreendimento__empreendimento=empree

def camp_full(metodo, campanha, empree):
	if len(Levantamentos.objects.filter(metodo__metodo__metogrup__metodo__metodo=metodo,campanha__num_campanha=campanha,campanha__empreendimento__empreendimento=empree))!=0:
		return ('campanha com levantamentos. Para fazer upload nessa campanha, voce precisa apagar todos os levantamentos dela. Cuidado com esse procedimento!','erro')
	else:
		return ('campanha com levantamentos', 'ok')

def verifica(lista=None,instdoc=None):
	ll_erro=[]
	for i in lista:
		metodo=list(i[0].split('/'))[-2]
		var_biodiv=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento__empreendimento=instdoc.empreendimento).var_biodiv
		var_esfor=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento__empreendimento=instdoc.empreendimento).var_esfor
		lt_biodiv=[bio for bio in list(var_biodiv.split(','))]
		lt_esfor=[esf for esf in list(var_esfor.split(','))]
		ll=[]
		for ii in i[1]:
			ll.append(os.path.join(i[0],ii))
		for way3 in ll:
			camp_ful=camp_full(metodo, int(way3.split('/')[-2]),instdoc.empreendimento)
			if camp_ful[1]=='ok':
				with open(way3, 'r') as file0:
					file1=file0.readlines()
				file2=[a for a in file1 if a != '\n'];file2=[i.replace('\"','') for i in file2]
				file2=[i.replace('\n','') for i in file2];file2=[i.replace('\r','') for i in file2]
				file3=[b for b in [i.split(',') for i in file2]]
				if 'biodiv' in way3:
					file_biodiv=file3
					lt_bio=listalista(lt_biodiv,file_biodiv)
					lt_bio=[lti for lti in lt_bio if lti not in EMPTY_VALUES]
					if lt_bio not in EMPTY_VALUES:
						ll_erro.append(['metodo: %s' %metodo,'campanha: %s'%way3.split('/')[-2],lt_bio])
	#			print 'll_erro',ll_erro
		#		print 'lt_bio',lt_bio
		#		print 'file_biodiv',file_biodiv
				elif 'esfor' in way3:
					file_esfor=file3
					lt_esf=listalista(lt_esfor,file_esfor)
					lt_esf=[lti for lti in lt_esf if lti not in EMPTY_VALUES]
					erro_dupli_levant=levant_dupli(file_esfor)
					if lt_esf not in EMPTY_VALUES:
						ll_erro.append(['metodo: %s'%way3.split('/')[-3],'campanhas: %s'%way3.split('/')[-2],lt_esf])
					if erro_dupli_levant[1]=='erro':
						ll_erro.append(['metodo: %s'%way3.split('/')[-3],'campanhas: %s'%way3.split('/')[-2],erro_dupli_levant[0]])
			else:
				ll_erro.append(['metodo: %s'%way3.split('/')[-3],'campanhas: %s'%way3.split('/')[-2],camp_ful[0]])
		#		print 'll_erro',ll_erro
		#		print 'lt_bio',lt_bio
	print u'll_erro: %s'%ll_erro
	print u'll: %s' %ll
	return ll,ll_erro

def eraselevant(request, empree):
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		preeraselevant=Campanhas.objects.all()
		context=RequestContext(request, {'preeraselevant':preeraselevant, 'empree':empree})
		return render_to_response('eraselevant.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})
def erasecamp(request, empree):
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		preerasecamp=Campanhas.objects.all()
		context=RequestContext(request, {'preerasecamp':preerasecamp, 'empree':empree})
		return render_to_response('erasecamp.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})

def del_leva(request, pk, empree=None):
	f=Campanhas.objects.get(id=pk)
	print 'f: %s' %f
	num_camp=int(f.num_campanha)
	print 'num_camp: %s'%str(f.num_campanha)
	met=f.metodo.metodo.metogrup.metodo.metodo
	l1=Levantamentos.objects.filter(campanha=f)
	print 'del_leva'
	for i in l1:
		i.delete()
	context=RequestContext(request, {'num_camp':num_camp, 'met':met, 'empree':empree})
	return render_to_response('deletadalevacampanha.html',context)

def del_camp(request, pk, empree=None):
	f=Campanhas.objects.get(id=pk)
	print 'f: %s' %f
	num_camp=int(f.num_campanha)
	print 'num_camp: %s'%str(f.num_campanha)
	met=f.metodo.metodo.metogrup.metodo.metodo
	l1=Levantamentos.objects.filter(campanha=f)
	print 'del_camp'
	for i in l1:
		i.delete()
	f.delete()
	context=RequestContext(request, {'num_camp':num_camp, 'met':met, 'empree':empree})
	return render_to_response('deletadacampanha.html',context)
def levant_dupli(file_esfor):
	l=[]
	for i in file_esfor:
		del i[0]
		if i not in l:
			l.append(i)
	if len(l)!=len(file_esfor):
		return ([u'Inconsistência! Dois levantamentos exatamente iguais nessa campanha.'], 'erro')
	return ('1','ok')

def listalista(lt_geral,file3):
	lt_erro_campo=[]
	for i in lt_geral:
		i=i.strip()
		try:
			atr=Atributos.objects.get(nome_atributo_cabecalho_coluna=i)
		except:
			print 'nao tem tal o atributo --%s--'%i	
			context={'umatributo':'nao tem tal o atributo --%s--'%i}
			return render_to_response('pg_erro_inclusao_dados_biodiv.html',context)
		dic=dic_tipo_vlr_test[atr.tipo_valor]
		posicao=lt_geral.index(i)
		lt_float=[];lt_stri=[];lt_inte=[];lt_data=[];lt_time=[]
		if atr.tipo_valor!='6':
			for con,ii in enumerate(file3):
				if not ii[posicao] in EMPTY_VALUES:
					if atr.tipo_valor=='5':
						try:
							i3=alteratime(ii[posicao])
						except:
							if not i3 in EMPTY_VALUES:
								lt_time.append(['o atributo: -%s- precisa ser: %s' %(i,dic_tipo_vlr[atr.tipo_valor]),'linha: %s'%(con+1),'coluna: %s'%posicao,'valor errado: %s'%ii[posicao],'tipo: %s'%type(ii[posicao])])
							print '%s nao esta de acordo com o especificado'%ii[posicao]
					elif atr.tipo_valor=='1':
						try:
							 i3=alteradata(ii[posicao])
						except:
							if not i3 in EMPTY_VALUES:
								lt_data.append()
							print '%s nao esta de acordo com o especificado'%ii[posicao]
					elif atr.tipo_valor=='4': 
						try:
							i3=int(ii[posicao])
						except:
							if not i3 in EMPTY_VALUES:
								lt_inte.append(['o atributo: -%s- precisa ser: %s' %(i,dic_tipo_vlr[atr.tipo_valor]),'linha: %s'%(con+1),'coluna: %s'%posicao,'valor errado: %s'%ii[posicao],'tipo: %s'%type(ii[posicao])])
							print '%s nao esta de acordo com o especificado'%ii[posicao]
					elif atr.tipo_valor=='3':					
						try:
							i3=str(ii[posicao])
						except:
							if not i3 in EMPTY_VALUES:
								lt_stri.append(['o atributo: -%s- precisa ser: %s' %(i,dic_tipo_vlr[atr.tipo_valor]),'linha: %s'%(con+1),'coluna: %s'%posicao,'valor errado: %s'%ii[posicao],'tipo: %s'%type(ii[posicao])])
							print '%s nao esta de acordo com o especificado'%ii[posicao]
					elif atr.tipo_valor=='2':
						try:
							i3=float(ii[posicao])
						except:
							if not i3 in EMPTY_VALUES:
								lt_float.append(['o atributo: -%s- precisa ser: %s' %(i,dic_tipo_vlr[atr.tipo_valor]),'linha: %s'%(con+1),'coluna: %s'%posicao,'valor errado: %s'%ii[posicao],'tipo: %s'%type(ii[posicao])])
							print '%s nao esta de acordo com o especificado'%ii[posicao]
			lt_erro_campo.append([i for i in lt_float if i not in EMPTY_VALUES]+[i for i in lt_stri if i not in EMPTY_VALUES]+[i for i in lt_inte if i not in EMPTY_VALUES]+[i for i in lt_data if i not in EMPTY_VALUES]+[i for i in lt_time if i not in EMPTY_VALUES])
	return lt_erro_campo

def montaup(docbiodiv5,docesfor5,instdoc,campanha,metodo):
	docbiodiv4=[i1.replace('\"','') for i1 in docbiodiv5]
	docbiodiv3=[i1.replace('\n','') for i1 in docbiodiv4]
	docbiodiv2=[i1.replace('\r','') for i1 in docbiodiv3]
	docbiodiv1=[b for b in [i1.split(',') for i1 in docbiodiv2]]
	docbiodiv0=[a for a in docbiodiv1 if a != '\n']
	docbiodiv=[a for a in docbiodiv0 if a != '\r']
	docesfor4=[i1.replace('\"','') for i1 in docesfor5]
	docesfor3=[i1.replace('\n','') for i1 in docesfor4]
	docesfor2=[i1.replace('\r','') for i1 in docesfor3]
	docesfor1=[b for b in [i.split(',') for i in docesfor2]] 
	docesfor0=[a for a in docesfor1 if a != '\n']
	docesfor=[a for a in docesfor0 if a != '\r']

#pega o cabecalho da planilha
	ca_biodiv=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento=instdoc.empreendimento).var_biodiv
	ca_esfor=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento=instdoc.empreendimento).var_esfor
#sanitiza o cabecalho da planilha
	ca_biodiv=list(ca_biodiv.split(','))
	ca_esfor=list(ca_esfor.split(','))
#sanitiza os dados dos arquivo biodiv e esfor
	dic_biodiv=montadic_zip(docbiodiv,ca_biodiv,metodo,campanha,instdoc.empreendimento)
	dic_esfor=montadic_zip(docesfor,ca_esfor,metodo,campanha,instdoc.empreendimento)
	#	iinstancia vem de outra view
	return (dic_biodiv,dic_esfor,ca_esfor)

def anadois(treedir):
	respok=[]
	responk=[]
	for d,f,fl in os.walk(treedir):
		if not f:
			if len(fl)==2:
				g=''.join(fl)
			else:
				responk.append((d, 'sem os dois arquivos'))
				g=[]
			if 'biodiv' and 'esfor' in g and responk==[]:
				respok.append((d,fl))
	if not responk in EMPTY_VALUES:
		return (responk,'erro')
	return (respok,'ok')

def extractzip(instdoc,treedir):

	docstr=instdoc.docfile.name
	ar1=ZipFile(docstr,'r')
	for i in ar1.namelist():
		if not i.endswith('/'):
			il=i.split('/')
			ij='/'.join([il[-3],il[-2],''])
			os.system('mkdir %s/%s'%(treedir,il[-3]))
			os.system('mkdir %s/%s/%s'%(treedir,il[-3],il[-2]))
			uf=ar1.read(i)
			try:
				of=open('%s/%s/%s/%s'%(treedir,il[-3],il[-2],il[-1]),'w')
				of.write(uf);of.close()
			except: pass

def inputafile(way,instdoc,ori,dst):
	if ori=='bioticos':
		destino=os.path.join(way,dst)
		nomefile=str(datetime.now()).replace(' ','_').replace(':','_')+'___bioticos.zip'
		nomefile_way='empreendimentos/%s/%s/%s'%(instdoc.empreendimento,dst,nomefile)
	else: pass

	shutil.move(instdoc.docfile.name,nomefile_way)
	instdoc.docfile=nomefile_way
	instdoc.save()
	dirfile=nomefile_way.split('/')[-1].strip('.zip')
	treedir=way+'/'+ori+'/'+dirfile
	os.system('mkdir %s'%treedir)
	return instdoc,treedir
@login_required
def importfolder(request, empree, modd=None, cab=None, ca=None):
	#print 'request: %s'%request
	print 'chegou no importfolder'
	if request.method == 'POST':
		form = DocumentZipForm(request.POST, request.FILES)
		if form.is_valid():
			instdoc=form.save()
			print instdoc.docfile.name
			instdoc.empreendimento=Empreendimentos.objects.get(empreendimento=empree)
			print instdoc.docfile.name
			instdoc.save()
			print instdoc.docfile.name
			way='empreendimentos/%s' %instdoc.empreendimento
			print way
			global instdoc, treedir
			instdoc,treedir=inputafile(way,instdoc,'bioticos','zips')
			extractzip(instdoc,treedir)
			global lista
			listaa=anadois(treedir)
			if listaa[1]=='erro':
				context=RequestContext(request,{'lista_erro':listaa[0]})
				return render_to_response('get_file_ziperro.html', context)
				return HttpResponse('erro na lista')
			lista=listaa[0]
			print u'instdoc.docfile.name: %s'%instdoc.docfile.name
			print u'instdoc.empreendimento: %s'%instdoc.empreendimento
			print u'treedir: %s'%treedir
			print u'way: %s'%way
			print u'instdoc.docfile.name; %s'%instdoc.docfile.name
			lt_files,lt_error=verifica(lista,instdoc)
			if lt_error not in EMPTY_VALUES:
				print u'len(lt_error): %s'%len(lt_error)
				lt_error=[i for i in lt_error if i not in EMPTY_VALUES]
				context=RequestContext(request,{'lista_erro':lt_error})
				return render_to_response('get_file_ziperro.html', context)
			else:
				return HttpResponseRedirect(reverse('dados:uploaddata',kwargs={'empree':empree}))
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		documents=Document.objects.all()
		form=DocumentZipForm()#{'empreendimento':'teste1'})
		context=RequestContext(request,{'documents':documents, 'modd':'AB', 'form':form,'empree':empree, 'modd':str(modd)})
		return render_to_response('get_file_zip.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})

def uploaddata(request, empree=None):
	return render_to_response('get_file_zip2.html', {'empree':empree})

def retirapop(request):
	global instdoc,treedir,lista
	lista_upES=[];listaimport=[]
	for i in lista:
		g=list(i[0].split('/'))
		if g[-1] in EMPTY_VALUES: del g[-1]
		campanha=g[-1]
		metodo=g[-2]
		iid=Campanhas.objects.get(metodo__metodo__metogrup__metodo__metodo=metodo,num_campanha=int(campanha),empreendimento=Empreendimentos.objects.get(empreendimento=instdoc.empreendimento.empreendimento)).id
		print 'id da Campanha: %d'%iid
		#pega as planilhas biodiv e esfor
		for ii in i[1]:
			if 'biodiv' in ii:
				b='b'
				with open(i[0]+'/'+ii, 'r') as biodiv:
					docbiodiv5=biodiv.readlines()
			if 'esfor' in ii:
				e='e'
				with open(i[0]+'/'+ii, 'r') as esfor:
					docesfor5=esfor.readlines()
		if b=='b' and e=='e':
			listaimport.append(iid)
		montp=montaup(docbiodiv5,docesfor5,instdoc,campanha,metodo)

		#if not montp[0] in EMPTY_VALUES and montp[1] in EMPTY_VALUES:
		upES=upESF(montp[0],montp[1],instdoc, metodo,montp[2],campanha)
		if upES not in EMPTY_VALUES:
			lista_upES.append(upES)
	print 'listaimport completa: %s' %listaimport
	lt_upES=[lies for lies in lista_upES if lies not in EMPTY_VALUES]
	empree=instdoc.empreendimento
	if lt_upES in EMPTY_VALUES:
		return HttpResponseRedirect(reverse('dados:succok', kwargs={'empree': empree,'lista':listaimport}))
	else:
		context={'lt_upES':lista, 'empree':empree}
		return render_to_response('problemas_or_success.html',context)

def succok(request, lista=None, empree=None):
	listimpo=[]
	print 'lista: %s'%lista
	print 'type(lista): %s'%type(lista)
	print 'type(eval(lista)): %s'%type(eval(lista))
	for i in eval(lista):
		camp=Campanhas.objects.get(id=i)
		frase=u'Método: %s, Campanha: %s'%(camp.metodo.metodo.metogrup.metodo,camp.num_campanha)
		listimpo.append(frase)
	context={'lt_import':listimpo, 'empree':empree}
	return render_to_response('problemas_or_success.html',context)

@transaction.commit_on_success
def upESF(dic_biodiv,dic_esfor,instdoc,metodo,ca_esfor,campanha):
	for k,v in dic_esfor.iteritems():
		dic_lev={};dic_other_lev={};dic_uaa={}
		dic_lev['metodo']=MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=metodo,metodo__empreendimento=instdoc.empreendimento)
		try:
			dic_lev['campanha']=Campanhas.objects.get(metodo__metodo__metogrup__metodo__metodo=metodo,empreendimento=instdoc.empreendimento, num_campanha=int(campanha))
		except: print 'nao conseguiu kk--campanha'
		if 'cod_ua' in ca_esfor:
			for kk,vv in v.iteritems():
				if kk in cab_lev:
					dic_lev[kk]=ifnone(vv)
				else:
					if kk=='data':
						dic_lev['dt_inicial']=alteradata(ifnone(vv))
						dic_lev['dt_final']=alteradata(ifnone(vv))
					elif 'dt_' in kk:
						dic_lev[kk]=alteradata(ifnone(vv))
					elif kk=='hora':
						dic_lev['hr_inicial']=alteratime(ifnone(vv))
						dic_lev['hr_final']=alteratime(ifnone(vv))
					elif kk=='temperatura':
						dic_lev['temp_inicial']=ifnone(vv)
						dic_lev['temp_final']=ifnone(vv)
					elif kk==['obs']:
						dic_lev['obs_l']=ifnone(vv)
					elif kk==['latitude']:
						dic_lev['lat_inicial']==ifnone(vv)
						dic_lev['lat_final']==ifnone(vv)
					elif kk==['longitude']:
						dic_lev['long_inicial']==ifnone(vv)
						dic_lev['long_final']==ifnone(vv)
					elif kk=='cod_ua':
						try:
							dic_lev['id_ua']=Parcelas.objects.get(nome=vv,trilha__grade_modulo__empreendimento=instdoc.empreendimento).id
							dic_lev['tipo_ua']=1
						except:
							try:
								dic_lev['id_ua']=Trilhas.objects.get(nome=vv,grade_modulo__empreendimento=instdoc.empreendimento.__dict__['id']).id
								dic_lev['tipo_ua']=5
							except: 
								return excecao(kk,vv, dic_lev)
								
					else:
						if kk !='id_provi':
							dic_other_lev[kk]=ifnone(vv)
		else:
			for kk,vv in v.iteritems():
				if kk in cab_uaa:
					dic_uaa[kk]=ifnone(ifnone(vv))
				dic_uaa['empreendimento']=instdoc.empreendimento
				if 'latitude' in v.keys():
					latlong='La_'+str(v['latitude'])+'Lo_'+str(v['longitude'])
				elif 'lat_inicial' in v.keys():
					latlong='La_'+str(v['lat_inicial'])+'Lo_'+str(v['long_inicial'])
				elif 'data' in v.keys():
					data=str(v['data'])	
				elif 'dt_inicio' in v.keys():
					data=str(v['dt_inicio'])	
				dic_uaa['nome']=str(instdoc.empreendimento)+latlong+data

			if not dic_uaa in EMPTY_VALUES:
				instUa=getcreate(UaAvulsas,dic_uaa)

			for kk,vv in v.iteritems():
				if kk in cab_lev:
					dic_lev[kk]=ifnone(vv)
				else:
					if kk=='data':
						dic_lev['dt_inicial']=alteradata(ifnone(vv))
						dic_lev['dt_final']=alteradata(ifnone(vv))
					elif 'dt_' in kk:
						dic_lev[kk]=alteradata(ifnone(vv))
					elif kk=='hora':
						dic_lev['hr_inicial']=alteratime(ifnone(vv))
						dic_lev['hr_final']=alteratime(ifnone(vv))
					elif kk=='temperatura':
						dic_lev['temp_inicial']=ifnone(vv)
						dic_lev['temp_final']=ifnone(vv)
					elif kk=='obs':
						dic_lev['obs_l']=ifnone(vv)
					elif kk=='latitude':
						dic_lev['lat_inicial']=ifnone(vv)
						dic_lev['lat_final']=ifnone(vv)
					elif kk=='longitude':
						dic_lev['long_inicial']=ifnone(vv)
						dic_lev['long_final']=ifnone(vv)
					elif kk !='id_provi':
						dic_other_lev[kk]=ifnone(vv)
					else:
						if kk !='id_provi':
							dic_other_lev[kk]=ifnone(vv)
					dic_lev['id_ua']=instUa.id
					dic_lev['tipo_ua']='6'

		if not dic_lev in EMPTY_VALUES:
			instL=getcreate(Levantamentos, dic_lev)
			atr_Abio_outros_erros=[];atr_Abio_erro_cadastro=[];grava_bio_erro=[];erro_do_update=[]
			for k3,v3 in dic_other_lev.iteritems():
				try:
					instATR=Atributos.objects.get(nome_atributo_cabecalho_coluna=k3)
				except:
					atr_Abio_erro_cadastro.append(k3)
				if instATR:
					instAb=pop_tbl_last(instATR=instATR,instAll=instL,valor=v3)#(inst=instL --> critico)
				else: pass
			instGeral=upBIO(dic_biodiv,instL=instL,id_proviL=v['id_provi'])
			#except:
			#	grava_bio_erro.append((k3,v3))
			if atr_Abio_erro_cadastro not in EMPTY_VALUES or atr_Abio_outros_erros not in EMPTY_VALUES or grava_bio_erro not in EMPTY_VALUES:
				erro_do_update.append((atr_Abio_erro_cadastro,atr_Abio_outros_erros,grava_bio_erro))
	if erro_do_update in EMPTY_VALUES:
		return instGeral
	else:
		return erro_do_update
		
def upBIO(dic_biodiv,instL,id_proviL):
	dic_provi= {}
	instGeral=[]
	for kb,vb in dic_biodiv.iteritems():
		if vb['id_provi']==id_proviL:
			dic_provi[kb]=vb
	for kb,vb in dic_provi.iteritems():
		dic_ani={};dic_pla={};dic_other_ani={};dic_other_pla={}
		for kkb,vvb in vb.iteritems():
			if kkb in cab_ani:
				dic_ani[kkb]=ifnone(vvb)
				dic_ani['levantamento']=instL.id
			elif kkb in cab_pla:
				dic_pla[kkb]=ifnone(vvb)
				dic_pla['levantamento']=instL.id
		if not dic_ani in EMPTY_VALUES:
			instA=saveform(AnimaisDados,dic_ani)
		if not dic_pla in EMPTY_VALUES:
			instP=saveform(PlantasDados,dic_pla)
		for kkb,vvb in vb.iteritems():
			if not kkb in dic_ani and not kkb in dic_pla:
				if kkb!='id_provi':
					if kkb!='cod_ua':
						try:
							instATR=Atributos.objects.get(nome_atributo_cabecalho_coluna=kkb)
						except: print 'o atributo %s nao esta cadastrado'%kkb
						try:
							if instA:
								if not instA in EMPTY_VALUES:
									instGA=pop_tbl_last(instATR=instATR,instAll=instA,valor=vvb)
									if not instGA in EMPTY_VALUES:
										instGeral.append(instGA)
						except: pass
						try:
							if instP:
								if not instP in EMPTY_VALUES:
									instGP=pop_tbl_last(instATR=instATR,instAll=instP,valor=vvb)
									if not instGP in EMPTY_VALUES:
										instGeral.append(instGP)
						except: pass
	return instGeral
	
def pop_tbl_last(instATR,instAll,valor):
#	if inst==instA:#critico
  #dic_tipo_vlr={'1':'Date','2':'Float','3':'Varchar','4':'Integer','5':'Time','6':'Text'}
#		sec_name=dic_tipo_vlr[instA.tipo_valor]
#		comp_name=eval('Animais'+sec_name)
#		instAa=comp_name(atributo=instATR.id,animais_dado=inst.id,valor=vv)
#		instAa.save()
	erro_save_tbl_finais=[]
	try:
		class_name=eval(dic_referencia[str(instATR.referencia)]+dic_tipo_vlr[instATR.tipo_valor])
		if 'nimai' in dic_referencia[instATR.referencia]:
			dii={'atributo':instATR,'animais_dado':instAll,'valor':valor}			
			inst1=getcreate(class_name,dii)
		elif 'lanta' in dic_referencia[instATR.referencia]:
			dii={'atributo':instATR,'plantas_dado':instAll,'valor':valor}
			inst1=getcreate(class_name,dii)
		elif 'biotic' in dic_referencia[instATR.referencia]:
			dii={'atributo':instATR,'abioticos_dado':instAll,'valor':valor}
			inst1=getcreate(class_name,dii)
	except:
		try:
			print 'nao formou: ou classe: %s -  ou campo %s. Atributo %s e dado tbl_baixa %s'%(dic_referencia[str(instATR.referencia)]+dic_tipo_vlr[instATR.tipo_valor], dic_referencia[instATR.referencia].lower()+'_dado', str(instATR), str(instAll))
		except:
			print 'nao identificado - %s - %s'%(str(instATR), str(instAll))
	try:
		erro_save_tbl_finais.append(inst1.errors)
	except: pass
	return erro_save_tbl_finais

def saveform(modd,dic):
	class my_form(forms.ModelForm):
		class Meta:
			model=modd
	inst=my_form(dic)
	if inst.is_valid():
		inst=inst.save()
	return inst

def getcreate(modd,dic):
	inst=modd.objects.get_or_create(**dic)
	return inst[0]

def alteratime(ti):
	if ':' in ti: s=':'
	elif '-' in ti: s='-'
	elif '.' in ti: s='.'
	ti=time(int(ti.split(s)[0]),int(ti.split(s)[1]))
	return ti
def alteradt(dt1):
	for k,v in dt1.iteritems():
		for kk,vv in v.iteritems():
			if 'dt_' in kk:vv=alteradata(vv)
	return dt1

def alteradata(dt):
	if '/'in dt:s='/'
	elif '.' in dt: s='.'
	elif '-' in dt: s='-'
	else: pass
	dt1=dt.split(s)
	if len(dt1[0])==4:
		return str(dt1[0]+'-'+dt1[1]+'-'+dt1[2])
	if len(dt1[0])!=4 and len(dt1[2])!=4:
		dt1[2]='20'+dt1[2]
		return str(dt1[0]+'-'+dt1[1]+'-'+dt1[2])  
	return str(dt.split(s)[2]+'-'+dt.split(s)[1]+'-'+dt.split(s)[0])

def ifnone(field):
	if field in EMPTY_VALUES:
		return None
	return field

	

def excecao(kk,vv,dic_lev):
	
	return render_to_response ('erro_Exception.html',{'chave':kk,'valor':vv,'dic_ate':dic_lev})

