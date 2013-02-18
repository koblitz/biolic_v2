#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from dados.forms import *
from dados.models import *
from gerencia.forms import *
from gerencia.models import *
from django.core.validators import EMPTY_VALUES
from django.core.urlresolvers import reverse
from django.db import transaction
import unicodedata
from django.shortcuts import get_object_or_404
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign
from guardian.decorators import permission_required

@login_required
def escolheform(request, formin=None):
	if request.method=='POST':
		return create(request)
	return new(request, formin)

def new (request, formin=None):
	if formin==EmpreendimentosForm:
		context=RequestContext(request,{'formg':formin})
	elif formin==Empreendimentos1Form:
		user=request.user
		userid=User.objects.get(username=user).id
		print 'user: %s'%user
		formin=Empreendimentos1Form(userid)
		context=RequestContext(request, {'form':formin})
	else:
		context=RequestContext(request, {'form':formin})
	return render_to_response('new.html', context)
#@permission_required('gerencia.alter_all_empree')
def create(request):
	try:
		cadastro=request.POST.get('cadastrar',None)
	except: pass
	if cadastro is not None:
		user=request.user
		new_post=request.POST.copy()
		new_post.update({'created_by':user.id})
		cadastrar=EmpreendimentosForm(new_post)
		if cadastrar.is_valid():
			empree=cadastrar.save()
			content_type = ContentType.objects.get(app_label='dados', model='empreendimentos')
			permission = Permission.objects.get_or_create(codename='alter_all_empree',name='Altera Tudo deste Empreendimento', content_type=content_type)
			assign('alter_all_empree',user,empree)
			print 'permission; %s'%permission[0]
			cria_dirs(empree)
			return HttpResponseRedirect(reverse('gerencia:successEmpree', kwargs={'empree':empree}))
		else:
			return render_to_response('erroformin.html',{'erro':cadastrar.errors})

	else:
		consultar=request.POST.get('consultar', None)
		gerenciar=request.POST.get('gerenciar', None)
		#empree=Empreendimentos1Form(request.POST)
		empree=request.POST.get('empreendimento', None)
		empree=Empreendimentos.objects.get(id=empree)
		user=request.user
		context=RequestContext(request,{'empree':empree})
		if gerenciar:
			print 'request.user antes do if: %s'%user
			if not user.has_perm('alter_all_empree',empree):
				#print 'request.user: %s'%request.user
				return render_to_response('pego.html',{'metemp':'SEM_PERM'})
			else:
				#return render_to_response('pego.html',	{'metemp':'COM_PERM'})
				return render_to_response('gerenciar.html',context)
		if consultar:
			return HttpResponseRedirect(reverse('consultar:consinicial', kwargs={'empree':empree}))

	context=RequestContext(request,{'new':new})
	return render_to_response('sucesso.html', context)

def success(request,empree,strmodd,modd):
	if strmodd=='empreendimento':
		cadastrado=get_object_or_404(Empreendimentos,empreendimento=empree)
	else: pass
	cadstradostr=cadastrado.__dict__[strmodd]
	context=RequestContext(request,{'cadastrado':cadstradostr,'strmodd':strmodd})
	return render_to_response('sucesso.html',context)

def cria_dirs(empree):
	way='empreendimentos/%s'%empree
	if not os.path.isdir(way)==True:
		os.system('mkdir %s' % way)
		os.system('mkdir %s/bioticos' %way)
		os.system('mkdir %s/shapes' %way)
		os.system('mkdir %s/altualizacoes' %way)
		os.system('mkdir %s/estrutura_geral' %way)
		os.system('mkdir %s/zips' %way)
	else:
		print 'o empreendimento ja esta cadastrado'
		mensagem= 'o empreendimento %s ja esta cadastrado' %empree
		return render_to_response('erro.html', {'erro': mensagem})

def montadic(modd,doc1, empree=None, ca=None, cab=None):
	doc2=[]
	#return render_to_response('pego.html',{'metemp':'tem'})
	if modd==GradesModulos:
		for i in doc1:
			b=[ii for ii in list(i.split(','))]
			doc2.append(b)
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)
		#return render_to_response('pego.html',{'metemps':dt1})

	if modd==Trilhas:
		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==0:
					try:
						b.append(GradesModulos.objects.get(abrev__iexact=ii[1], empreendimento__empreendimento=empree).id)
					except:
						pass#print 'erro na consulta no GradesModulos'

				else:
					b.append(ii[1])
			doc2.append(b)
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
	
	if modd==Parcelas:
#se ultima letra for uma ',' delete obs no 'ca'
#SAAT-IP-T1,SAAT-IP-T1-0000,10,0,TRUE,250,
		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==0:
					try:
						b.append(Trilhas.objects.get(nome__iexact=ii[1],grade_modulo__empreendimento__empreendimento=empree).id)
					except:
						b.append('')
						#pass#print 'erro na consulta no GradesModulos'
				else:
					b.append(ii[1])
			doc2.append(b)
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))

	if modd==Coordenadas:
#SAAT-IP-T1-1000 ,-9.18178 ,-64.6184 ,inicio
#coordenadasca:ref,latitude,longitude,localidade
#coordenadascab-ref,latitude,longitude,localidade,empreendimento
		for i in doc1:
			g=list(i.split(','))
			b=[ii for ii in g]
			doc2.append(b)
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)

	if modd==Campanhas:
#avifauna,aves_rede,,15/03/2010,30/03/2010,7.43,25.7,1
#Herpetofauna,pitfall_herp,Marcos Croci,28/07/09,03/01/10,120,20,1 
		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==1:#MPP
					try:
						b.append(MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=ii[1],metodo__empreendimento__empreendimento=empree).id)
						print MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=ii[1],metodo__empreendimento__empreendimento=empree).id
					except:	
						erro='precisa cadastrar o método %s'%ii[1]
						print erro
						print MPP.objects.get(metodo__metogrup__metodo__metodo__iexact=ii[1],metodo__empreendimento__empreendimento__iexact=empree).id
				elif ii[0]==2:#pessoa_responsavel
					if not ii[1] in EMPTY_VALUES:
						k=Pessoas.objects.get_or_create(pessoa=ii[1])
						b.append(k[0].id)
					else:
						k=Pessoas.objects.get_or_create(pessoa='nao_informada')
						b.append(k[0].id)
				elif ii[0]!=0:
					b.append(ii[1])
			doc2.append(b)
		#return render_to_response('pego.html',{'metemp':str(doc2)})
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)
	if modd==Topografias:
#cod_ua,latitude,longitude,valor,dist_perpendicular_trilha,coletor-->it
#coordenada_id,alt_mar,dist_perpend_trilha,coletor_emp,coletor_pess
#coordenada,alt_mar,dt_observacao,dist_perpend_trilha,coletor_emp,coletor_pess
#ref,coordenada,alt_mar,dist_perpend_trilha,coletor_emp,coletor_pess-->ca

		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==1: lat=ii[1]
				elif ii[0]==2:
					lon=ii[1]
					try:
						k=Coordenadas.objects.get_or_create(latitude=lat, longitude=lon, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
						b.append(k[0].id)
					except:
						print 'erro ao criar automaticamente id_coordenada pela Topografia'
				elif ii[0]==5: 
					coletor=ii[1]
					try:
						k=Pessoas.objects.get(pessoa__icontains=coletor, empreendimento__empreendimento=empree)
						b.append('')
						b.append(k.id)
					except:
						try:
							k=Empresas.objects.get_or_create(empresa=coletor, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
							b.append(k[0].id)
						except:
							print 'problemas no create Empresas pela topografia'
				else:
					b.append(ii[1])
			doc2.append(b)
		#return render_to_response('pego.html',{'metemp':str(doc2)})
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)
	if modd==Inclinacoes:
#coordenada,empreendimento,ref,dist_prepend_trilha,inclinacao,dt_observacao-->bd
#cod_ua,latitude,Longitude,dt_marcacao,valor,dist_perpendicular_trilha,coletor-->it
#ref,coordenada,dt_observacao,inclinacao,dist_prepend_trilha,coletor_emp,coletor_pess-->ca
#ref,coordenada,dt_observacao,inclinacao,dist_prepend_trilha,coletor_emp,coletor_pess,empreendimento-->cab
		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==1: lat=ii[1]
				elif ii[0]==2:
					lon=ii[1]
					try:
						k=Coordenadas.objects.get_or_create(latitude=lat, longitude=lon, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
						b.append(k[0].id)
					except:
						print 'erro ao criar automaticamente id_coordenada pela Topografia'
				elif ii[0]==6: 
					coletor=ii[1]
					try:
						k=Pessoas.objects.get(pessoa__icontains=coletor, empreendimento__empreendimento=empree)
						b.append('')
						b.append(k.id)
					except:
						try:
							k=Empresas.objects.get_or_create(empresa=coletor, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
							b.append(k[0].id)
						except:
							print 'problemas no create Empresas pela topografia'
				else:
					b.append(ii[1])
			doc2.append(b)
		#return render_to_response('pego.html',{'metemp':str(doc2)})
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)

	if modd==Solos:
#cod_ua,Latitude,Longitude,dt_marcacao,componente_solo,Valor,dit_perpendicular_trilha,coletor -->it
#coordenada,empreendimento,ref,dist_perpend_trilha,atributo,vlr,dt_observacao,coletor_emp,coletor_pess-->bd
#ref,coordenada,dt_observacao,atributo,vlr,dist_perpend_trilha,coletor_emp,coletor_pess-->ca
#ref,coordenada,dt_observacao,atributo,vlr,dist_perpend_trilha,coletor_emp,coletor_pess,empreendimento-->cab

		for i in doc1:
			g=list(i.split(','))
			b=[]
			for ii in enumerate(g):
				if ii[0]==1: lat=ii[1]
				elif ii[0]==2:
					lon=ii[1]
					try:
						k=Coordenadas.objects.get_or_create(latitude=lat, longitude=lon, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
						b.append(k[0].id)
					except:
						print 'erro ao criar automaticamente id_coordenada pela Topografia'
				elif ii[0]==4:
					componente=transminus(ii[1])
					try:
						componente_solo=Atributos.objects.get(nome_atributo_cabecalho_coluna__iexact=componente).id
						b.append(componente_solo)
					except:
						print 'Insira %s na tabela de atributos' %ii[1]
				elif ii[0]==7: 
					coletor=ii[1]
					try:
						k=Pessoas.objects.get(pessoa__icontains=coletor, empreendimento__empreendimento=empree)
						b.append('')
						b.append(k.id)
					except:
						try:
							k=Empresas.objects.get_or_create(empresa=coletor, empreendimento=Empreendimentos.objects.get(empreendimento=empree))
							b.append(k[0].id)
						except:
							print 'problemas no create Empresas pela topografia'
				else:
					b.append(ii[1])
			doc2.append(b)
		#return render_to_response('pego.html',{'metemp':str(doc2)})
		dt1={}
		for v,i in enumerate(doc2):
			dt1['line%s'%v]=dict(zip(ca,i))
		empree=Empreendimentos.objects.get(empreendimento=empree)
		for k,v in dt1.iteritems():
			v.update(empreendimento=empree.id)
#---------
	dt1=alteradt(dt1)
	return dt1
@login_required
@transaction.commit_on_success
def importgeral(request, empree=None, modd=None, cab=None, ca=None):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		empreestr=str(empree)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save();docdoc=open(newdoc.docfile.path, 'r')
			doc=docdoc.readlines();
			# correcao para tirar linhas nulas do doc 
			doc1=[a for a in doc if a != '\n'];doc1=[i.strip() for i in doc1];#doc1=[i.replace(' ','') for i in doc1]
			#return render_to_response('pego.html',{'metemp':str(modd)})
			dt1=montadic(modd,doc1,empree, ca)
			#return render_to_response('pego.html',{'metemps':dt1})
			class my_form(forms.ModelForm):
				class Meta:
					model=modd
					fields=tuple(cab)
			#return render_to_response('pego.html',{'form':my_form})
			salvoslt=[]
			for k,v in dt1.iteritems():
				f=my_form(v)
				if not f.is_valid():
					return render_to_response('erro.html',{'erro':f.errors, 'outroerro':'outroerro'})
				inst=f.save()
				salvoslt.append(f.cleaned_data)
				if modd==Coordenadas or modd==Topografias or modd==Inclinacoes:
					poeupdate(inst.pk, modd, empree)
			context=RequestContext(request,{'salvos':salvoslt})
			return render_to_response('recemsalvo.html', context)
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		documents=Document.objects.all()
		form=DocumentForm()
		context=RequestContext(request,{'documents':documents,'form':form,'empree':empree, 'modd':str(modd)})
		return render_to_response('get_file.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})

def verdoc(request):
	if request.method=='POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			docdoc=open(newdoc.docfile.path, 'r')
			doc=docdoc.readlines()
			context=RequestContext(request,{'newdoc':doc})
			return render_to_response ('show_file.html',context)
	else:
		form = DocumentForm() # A empty, unbound form
	# Load documents for the list page
	documents = Document.objects.all()
	# Render list page with the documents and the form
	return render_to_response('get_file.html',
		{'documents': documents, 'form': form},
		context_instance=RequestContext(request))

def cablocal(modelo,c):
	dt={};
	if c=='ca':
		ca=modelo+'ca';f=CabecalhosLocais.objects.get(modelo=ca);dt[f.modelo]=list(f.lista_campo.split(','));
		return dt[f.modelo]
	if c=='cab':
		cab=modelo.lower()+'cab';fb=CabecalhosLocais.objects.get(modelo=cab);dt[fb.modelo]=list(fb.lista_campo.split(','))
		return dt[fb.modelo]

def poeupdate(inst_pk,modd, empree):
	obj=modd.objects.get(id=inst_pk)

	#cl=modd();ncl=cl.__class__.__name__.lower();nc=ncl[:-1]
	try:
		t=Trilhas.objects.get(nome__iexact=obj.ref,grade_modulo__empreendimento__empreendimento=empree)
	except:
		try:
			p=Parcelas.objects.get(nome__iexact=obj.ref,trilha__grade_modulo__empreendimento__empreendimento=empree)
		except:
			u=UaAvulsas.objects.get(nome__iexact=obj.ref,empreendimento__empreendimento=empree)
	if modd==Coordenadas:
		try:
			u.coordenada.add(obj)
		except:
			try:
				p.coordenada.add(obj)
			except:
				t.coordenada.add(obj)
	if modd==Topografias:
		try:
			u.topografia.add(obj)
		except:
			try:
				p.topografia.add(obj)
			except:
				t.topografia.add(obj)
		
	if modd==Inclinacoes:
		try:
			u.inclinacao.add(obj)
		except:
			try:
				p.inclinacao.add(obj)
			except:
				t.inclinacao.add(obj)

def alteradado(dt):
#'%Y-%m-%d',       # '2006-10-25'
#'%m/%d/%Y',       # '10/25/2006'
#'%m/%d/%y',
	if '-' in dt:
		l=[i for i in dt.split('-')]
	if '/' in dt:
		l=[i for i in dt.split('/')]
	if '.' in dt:
		l=[i for i in dt.split('.')]
	try:
		ll=[];ll.append(l[1]);ll.append(l[0]);ll.append(l[2]);ls=''
		for i in ll:
			ls=ls+i+'/'
		ls=ls[:-1]
	except:
		ls=dt
	return ls

def alteradt(dt1):
	for i in dt1.items():
		for k,v in i[1].iteritems():
			if 'dt_' in k: i[1][k]=alteradado(v)
	return dt1

def transminus(input_str):
 nkfd_form = unicodedata.normalize('NFKD', unicode(input_str, 'utf8'))
 return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])





