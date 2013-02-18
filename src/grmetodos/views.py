#-*- coding: utf-8 -*-
from dados.models import *
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from forms import *
from dados.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core import validators
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms.formsets import formset_factory
import csv
from django.utils.encoding import smart_str, smart_unicode
from django.core.validators import EMPTY_VALUES
from django.template.loader import render_to_string
from django.utils import simplejson
import random
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelform_factory
from django.utils.functional import curry
from itertools import izip
from django.contrib.auth.decorators import login_required

@login_required
def escolheform(request, form1=None, empree=None):
	#try:
	#	empree=request.session.get('empree')
	#except: pass

	if request.method=='POST':
		metoesta=request.POST.getlist('fm0-metoesta', None)
		metoestat=request.POST.get('metoestat', None)
		metodoadm=request.POST.getlist('metodoadm', None)
	#	metodoadm1=request.POST.get('metodoadm1', None)
		arraestaespa=request.POST.getlist('form0-arraespaesta', None)
	#	metoestar=request.POST.getlist('metoestar',None)
		print 'aqui eh pos POST e o empree eh: %s'%empree
		print 'aqui eh pos POST e o metodoadm eh: %s'%metodoadm
		if metoesta or metoestat or arraestaespa:
			return createmonta(request, MontaEstaEspasForm, MontaEstaTempsForm,empree)
		if empree and metodoadm:
			print 'esse eh o metodoadm: %s' %metodoadm
			return createpremet(request, empree, metodoadm)	
		else:
			#return create(request, form1)
			return render_to_response('errotestegr.html',{'metemp':'escolha algum metodo!'})
	return new(request, form1, empree)
@login_required
def new (request, form1=None, empree=None):
	user=request.user
	print 'user: %s'%request.user
	print 'empree: %s'%empree
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	print 'empree1: %s'%empree1
	if user.has_perm('alter_all_empree',empree1):
		print 'tem pem'
		if form1==MetodosadmForm:
			mpp=MPP.objects.filter(metodo__empreendimento__empreendimento=empree)
			context=RequestContext(request, {'form':form1, 'empree':empree,'mpp':mpp})
			return render_to_response('newgr.html', context)
		if form1=='apagar':
			listametodos=MetoEmprs.objects.filter(empreendimento__empreendimento=empree)
			context=RequestContext(request, {'listametodos':listametodos,'empree':empree})
			return render_to_response('apagarmetodos.html',context)
		else:
			context=RequestContext(request, {'form':form1})
			return render_to_response('newgr.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})

@login_required
def create(request, form1=None):
	form1=form1(request.POST)
	if not form1.is_valid():
		return render_to_response('errotestegr.html',{'metemp':form1.errors})
	new=form1.save()
	context=RequestContext(request,{'new':new})
	return render_to_response('sucessogr.html', context)
@login_required
def createpremet(request, empree=None, metodo=None):
	user=request.user
	print 'user: %s'%user
	print 'metodo escolhido: %s'%metodo
	mpp_esc=[MPP.objects.get(id=i) for i in metodo]
	print 'mpp escolhido: %s'%mpp_esc
	metoempr_esc=[MetoEmprs.objects.get_or_create(metogrup=i.metodo.metogrup,empreendimento=Empreendimentos.objects.get(empreendimento=empree))[0] for i in mpp_esc]
	for i in MetoEmprs.objects.filter(empreendimento=Empreendimentos.objects.get(empreendimento=empree)):
		if i not in metoempr_esc:
			metoempr_esc.append(i)
	for i3 in metoempr_esc:
		MPP.objects.get_or_create(metodo=i3)
	return render_to_response('metodosempree.html',{'metoempr_esc':metoempr_esc,'empree':empree})
#	return render_to_reponse('preindexgr.html')

def defineestacao(request,empree,metogrup):
	if request.method=='POST':
		print 'request.POST: %s' %request.POST
		print 'metogrup no post: %s'%metogrup
		try:
			post1=formsetT(request.POST, prefix='tempo')
			if post1.is_valid():
				print 'POST1: %s'%post1
			else:
				print 'NAO PEGOU!!!!!'
		except: pass
#u'estacao1-0-arraespaesta': [u'21'], u'estacao1-0-arratempesta': [u'8'], 
		dictpost=request.POST.copy()
		die={};dit={};d1={}
	#	print 'dictpost: %s'%dictpost
		#d = {key: value for (key, value) in sequence}
		for k,v in dictpost.iteritems():
			if 'arraespaesta' in str(k):
				d1[k]=v
		print 'd1: %s'%d1
		ltTTES=[key for key in dictpost.iterkeys() if 'espaco' in str(key) and 'INITIAL_FORMS' not in str(key) and 'MAX_NUM_FORMS' not in str(key) and 'TOTAL_FORMS' not in str(key)]
		print 'ltTTES: %s'%ltTTES
		dEspa = {'%s'%key: request.POST.getlist(key) for key in ltTTES}
		print 'dEspa: %s'%dEspa
		ltArraEs=[key for key in dictpost.iterkeys() if 'espaco' in str(key) and 'arraespaesta' in str(key)]
		print 'ltArraEs: %s'%ltArraEs		
		for espa in ltArraEs:
			nomeesta=str(espa).replace('arraespaesta','metoesta')
			name=dEspa['%s'%nomeesta][0]
			for i in MetoEstas.objects.all():
				if str(i)==str(name):
					idd=i.id
			print 'idd: %s'%idd
			metoesta=MetoEstas.objects.get(id=idd)
			for es in dEspa['%s'%espa]:
				montaespa=MontaEstaEspas.objects.get_or_create(metoesta=metoesta,arraespaesta=ArraEspaEstas.objects.get(id=es))
				print 'montaespa: %s'%str(montaespa)
		ltTTTP=[key for key in dictpost.iterkeys() if 'tempo' in str(key) and 'INITIAL_FORMS' not in str(key) and 'MAX_NUM_FORMS' not in str(key) and 'TOTAL_FORMS' not in str(key)]
		print 'ltTTTP: %s'%ltTTTP
		dTemp = {'%s'%key: request.POST.getlist(key) for key in ltTTTP}
		print 'dTemp:%s'%dTemp
		ltArraTp=[key for key in dictpost.iterkeys() if 'tempo' in str(key) and 'arratempesta' in str(key)]
		print 'ltArraTp: %s'%ltArraTp
		for temp in ltArraTp:
			nomeesta=str(temp).replace('arratempesta','metoestat')
			name=dTemp['%s'%nomeesta][0]
			for i in MetoEstas.objects.all():
				if str(i)==str(name):
					idd=i.id
			print 'idd: %s'%idd
			metoesta=MetoEstas.objects.get(id=idd)
			for tm in dTemp['%s'%temp]:
				montatemp=MontaEstaTemps.objects.get_or_create(metoestat=metoesta,arratempesta=ArraTempEstas.objects.get(id=tm))
				print 'montatemp: %s'%str(montatemp)
		
		return HttpResponseRedirect(reverse('grmetodos:estac_compl', kwargs={'empree':empree,'metogrup':metogrup}))
	metogrup=MetoGrups.objects.get(id=metogrup)
	print 'metogrup: %s'%metogrup
	metoestaall=MetoEstas.objects.filter(metoempr__metogrup=metogrup,metoempr__empreendimento__empreendimento=empree)
	metoesta=[i.id for i in metoestaall]
	quantapetestalt=[QuantApetEstas.objects.filter(metoesta=me) for me in metoesta]
	montaestaespa=MontaEstaEspas.objects.filter(metoesta__metoempr__metogrup=metogrup,metoesta__metoempr__empreendimento__empreendimento='REFERENCIA')
	arraespaestalt=[]	
	for i in montaestaespa:
		if i.arraespaesta not in arraespaestalt:
			arraespaestalt.append(i.arraespaesta.id)
	montaestatemp=MontaEstaTemps.objects.filter(metoestat__metoempr__metogrup=metogrup,metoestat__metoempr__empreendimento__empreendimento='REFERENCIA')
	arratempestalt=[]	
	for i in montaestatemp:
		if i.arratempesta not in arratempestalt:
			arratempestalt.append(i.arratempesta.id)
	#MONTAFORMSET
	MontaEstaEspasFormSet=inlineformset_factory(MetoEstas,MontaEstaEspas,form=MetaMontaESForm, extra=len(metoesta),can_delete=False)
	MontaEstaEspasFormSet.form=staticmethod(curry(MetaMontaESForm,ltesf=arraespaestalt,metolt=metoesta))
	MontaEstaTempsFormSet=inlineformset_factory(MetoEstas,MontaEstaTemps,form=MetaMontaFSForm, extra=len(metoesta),can_delete=False)
	MontaEstaTempsFormSet.form=staticmethod(curry(MetaMontaFSForm,listlt=arratempestalt,metolt=metoesta))	
	dataT=[]; dataE=[]; apets=[]
	for cmetoesta in metoestaall:
		dt={'metoestat':cmetoesta}
		de={'metoesta':cmetoesta}
		dataT.append(dt)
		dataE.append(de)
		apets.append([QuantApetEstas.objects.filter(metoesta=cmetoesta)])
	formsetT=MontaEstaTempsFormSet(initial=dataT,prefix='tempo')
	formsetE=MontaEstaEspasFormSet(initial=dataE,prefix='espaco')
	bothforms=izip(formsetT,formsetE)
	context=RequestContext(request,{'empree':empree,'bothforms':bothforms,'apets':apets,'metoestaall':metoestaall,'metogrup':metogrup,'formsetT':formsetT, 'formsetE':formsetE})
	return render_to_response('defineestacao.html', context)

def estac_compl(request,empree,metogrup):
	metoestaall=MetoEstas.objects.filter(metoempr__metogrup=metogrup,metoempr__empreendimento__empreendimento=empree)
	ltmontaespa=[];ltmontatemp=[];metoestaltE=[];metoestaltT=[];ltmetoesta=[]
	montaestaf=MontaEstaEspas.objects.filter(metoesta__metoempr__metogrup=metogrup,metoesta__metoempr__empreendimento__empreendimento=empree).order_by('metoesta')
	for ii in MontaEstaTemps.objects.filter(metoestat__metoempr__metogrup=metogrup,metoestat__metoempr__empreendimento__empreendimento=empree).order_by('metoestat'):
		metoestaltT.append(ii)
	bothmontas=izip(metoestaltE,metoestaltT)
	context=RequestContext(request,{'ltmontaespa':montaestaf,'metoestaall':metoestaall,'bothmontas':bothmontas,'ltmetoesta':ltmetoesta,'ltmontatemp':metoestaltT})
	return render_to_response('estacoescompletas.html',context)


@login_required
def montamet(request, empree, metodoadm1=None):
	if request.method=='POST':
		#metodoadm1=Metodosadm1Form(request.POST)#.get('metodoadm1', None)
		metodoadm1=request.POST.get('metodoadm1', None)		
		print 'metodoadm1 agora com request.POST: %s'%metodoadm1
		metodoadm1=int(metodoadm1)
		#metodoadm1 é um número que é um id MetoEmprs 
		print 'metodoadm1: %s'%metodoadm1
		print 'type(metodoadm1): %s'%type(metodoadm1)
		metoemprr=MetoEmprs.objects.get(id=metodoadm1)
		print 'metoemprr: %s'%metoemprr
	#metoestaid = grupo de id de MetoEstas de empree.
		metss=MetoEstas.objects.filter(metoempr=metoemprr)
		metoesta_eeid=[i.id for i in metss]
		print 'metoesta_eeid: %s'%metoesta_eeid
		print 'metoemprr.metogrup.id: %s'%metoemprr.metogrup.id
		if metoesta_eeid not in EMPTY_VALUES:
			return HttpResponseRedirect(reverse('grmetodos:gerenciaestacao',kwargs={'empree':empree,'metogrup':metoemprr.metogrup.id,'metoesta_eeid':metoesta_eeid}))
	#se não tiver MetoEstas de empree - metoestaid ficara vazio.
		else:
			return HttpResponseRedirect(reverse('grmetodos:gerenciaestacao',kwargs={'empree':empree,'metogrup':metoemprr.metogrup.id}))
	print 'user: %s'%request.user
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		form=Metodosadm1Form(empree)
		context=RequestContext(request,{'form':form, 'empree':empree})
		return render_to_response('newgrdoempree.html',context)
	else:
		return render_to_response('erro_permissao.html',{'user':user,'empree':empree})
@login_required
def gerenciaestacao(request,empree,metogrup,metoesta_eeid=None, metoesta_ref=None):
	if request.method=='POST':
		print 'RREEQQUUEESSTT.POST: %s'%request.POST
		metoesta_refid=request.POST.getlist('metoesta_ref',None)
		concluir=request.POST.get('concluir',None)
		print 'metoesta_refid: %s'%metoesta_refid
		print 'empree: %s'%empree
		print 'metogrup: %s'%metogrup
		print 'concluir: %s'%concluir
		req=request.method
		print 'req: %s'%req#.META['REQUEST_METHOD']
		
		if not request.is_ajax():
			if 'concluir' and metoesta_refid in EMPTY_VALUES:
				return render_to_response('erro_atributo.html',{'semescolha':'voce tem que escolher uma opção de estação. Se isso não for necessário, essa etapa está concluída!'})
			if metoesta_refid not in EMPTY_VALUES:
				print 'metoesta_refid: %s'%metoesta_refid
				metoempr_ee=MetoEmprs.objects.get(metogrup=MetoGrups.objects.get(id=metogrup),empreendimento__empreendimento=empree)
				for i in metoesta_refid:
					metoesta_ref=MetoEstas.objects.get(id=i)
					r=random.randint(1000, 4000)
					print 'numero_aleatoreo: %s'%str(r)
					metoesta_new=MetoEstas.objects.get_or_create(metoempr=metoempr_ee,nome_estac='estacao'+str(r))
					metoesta_new=metoesta_new[0]
					print 'metoesta_new.id: %s'%metoesta_new.id
					quantapetesta_reflt=QuantApetEstas.objects.filter(metoesta=metoesta_ref)
					for qae in quantapetesta_reflt:
						QuantApetEstas.objects.get_or_create(metoesta=metoesta_new,apettipo=qae.apettipo,quantidade=qae.quantidade)
					nome_estac=nome_estacao(metoempr_ee)
					metoesta_new.nome_estac=nome_estac
					metoesta_new.save()
					print 'metoesta_new.nome_estac: %s'%metoesta_new.nome_estac
				#met_new.save()
				metoesta_eepost=MetoEstas.objects.filter(metoempr=metoempr_ee)
				quantapetesta_post=[QuantApetEstas.objects.filter(metoesta=m) for m in metoesta_eepost]
				metogrup1=MetoGrups.objects.get(id=metogrup)				
				context=RequestContext(request,{'empree':empree,'quantapetesta_post':quantapetesta_post,'metogrup':metogrup1})
				return render_to_response('estacoesexistentes2.html',context)
		else:
			metogrup_ref=MetoEstas.objects.get(id=metoesta_refid[0]).metoempr.metogrup
			metoempr_ee=MetoEmprs.objects.get(metogrup=metogrup_ref,empreendimento__empreendimento=empree)
			metoesta_ee=MetoEstas.objects.filter(metoempr=metoempr_ee)
			quantapetesta_ee=[QuantApetEstas.objects.filter(metoesta=metest1) for metest1 in metoesta_ee]
			quantapetesta_ee_lt=[]
			for q1 in quantapetesta_ee:
				quantapetesta_ee_lt.append([(ii.apettipo,ii.quantidade) for ii in q1 if not len(q1)==0])
			print 'quantapetesta_ee_lt: %s'%quantapetesta_ee_lt
			metoesta_ref=[MetoEstas.objects.get(id=i) for i in metoesta_refid]
			print 'metoesta_ref: %s'%metoesta_ref
			quantapetesta_ref=[QuantApetEstas.objects.filter(metoesta=metest2) for metest2 in metoesta_ref]
			print 'quantapetesta_ref: %s'%quantapetesta_ref
			quantapetesta_ref_lt=[]
			for q2 in quantapetesta_ref:
				quantapetesta_ref_lt.append([(ii.apettipo,ii.quantidade) for ii in q2 if not len(q2)==0])
			print 'quantapetesta_ref_lt: %s'%quantapetesta_ref_lt
			pre_coll_form=[i for i in quantapetesta_ref_lt if i not in quantapetesta_ee_lt]
			print 'pre_coll_form: %s'%pre_coll_form
			metest_temp=MetoEstas.objects.filter(metoempr__empreendimento__empreendimento='REFERENCIA',metoempr__metogrup=metoesta_ref[0].metoempr.metogrup)
			pre_coll_form2=[]
			for mt in metest_temp:
				for i in pre_coll_form:
					try:
						pre_coll_form2.append(QuantApetEstas.objects.get(apettipo=i[0][0],quantidade=i[0][1], metoesta=mt))
					except: pass
			print 'pre_coll_form2: %s'%pre_coll_form2
			metoesta_refid_pos=[i.metoesta.id for i in pre_coll_form2]
			print 'metoesta_refid_pos: %s'%metoesta_refid_pos
			coll_form_p_apaga=[QuantApetMetoEstasForm(idd) for idd in metoesta_refid_pos]
			context=RequestContext(request,{'coll_form_p_apaga':coll_form_p_apaga,'botao':'concluir montagem!'})
			print 'coll_form_p_apaga: %s'%coll_form_p_apaga
			html=render_to_string('gerenciaestacao2.html',context)
           	res={'html':html}
           	return HttpResponse (simplejson.dumps(res), mimetype='application/json')
	
	print 'type(metogrup): %s'%type(metogrup)
	print 'metoesta_eeid: %s'%metoesta_eeid
	if metoesta_eeid:
		print 'type(metoesta_eeid): %s'%type(metoesta_eeid)
		if type(metoesta_eeid)!=list:
			metoesta_eeid=list(metoesta_eeid.strip(']').strip('[').split(','))
	print 'type(metoesta_eeid): %s'%type(metoesta_eeid)
	metogrup_id=int(metogrup)
	
	print 'int(metogrup): %s'%int(metogrup)
	metogrup=MetoGrups.objects.get(id=metogrup_id)
	metoempr_ref=MetoEmprs.objects.get(metogrup=metogrup,empreendimento__empreendimento='REFERENCIA')
	coll_estacao_ref=MetoEstas.objects.filter(metoempr=metoempr_ref)
	print 'coll_estacao_ref: %s'%coll_estacao_ref
	metoesta_refid=[ii.id for ii in coll_estacao_ref]
	coll_form_ref=[QuantApetMetoEstasForm(idd) for idd in metoesta_refid]
	coll_apetrechos1=[]
	for ii in coll_estacao_ref:
		quantapetesta_ref_un=QuantApetEstas.objects.filter(metoesta=ii)
		for i3 in quantapetesta_ref_un:
			coll_apetrechos1.append(i3.apettipo.apetrecho)
	coll_apetrechos=[]
	for apet in coll_apetrechos1:
		 if apet not in coll_apetrechos:
			coll_apetrechos.append(apet)
	coll_apetdefis=[ApetDefis.objects.filter(apetrecho=apet) for apet in coll_apetrechos]
	print 'coll_apetdefis: %s'%coll_estacao_ref
	#se existe estacaoes para o empreendimento do metodo.
	if metoesta_eeid:
		metoesta_ee=[MetoEstas.objects.get(id=i) for i in metoesta_eeid]
		print 'metoesta_ee: %s'%metoesta_ee
		quantapetesta_ee=[QuantApetEstas.objects.filter(metoesta=i) for i in metoesta_ee if i not in EMPTY_VALUES]
		print 'quantapetesta_ee: %s'%quantapetesta_ee
		context=RequestContext(request,{'coll_apetdefis':coll_apetdefis,'coll_form_ref':coll_form_ref, 'empree':empree, 'quantapetesta_ee':quantapetesta_ee,'metogrup':metogrup})
	else:
		context=RequestContext(request,{'coll_apetdefis':coll_apetdefis,'coll_form_ref':coll_form_ref, 'empree':empree,'metogrup':metogrup})
	return render_to_response('gerenciaestacao.html', context)

def nome_estacao(metoempr):
	metoesta_g=MetoEstas.objects.filter(metoempr=metoempr)
	nomes=[int(str(i.nome_estac).strip('estacao')) for i in metoesta_g]
	print 'estacao'+str(min(nomes.index(i)+1 for i in nomes if nomes.index(i)+1!=i))
	return 'estacao'+str(min(nomes.index(i)+1 for i in nomes if nomes.index(i)+1!=i))
@login_required
def del_obj(request,pk=None, model1=None):
	
	data=get_object_or_404(model1,pk=pk)
	context=RequestContext(request,{'item':data})
	data1=str(data)
	print 'data1 pre delete: %s:'%data1
	data.delete()
	print 'data1 pos delete: %s'%data1
	model1=str(model1)
	print 'model1 pos str: %s'%model1
	if 'MetoEmprs' in model1:
		context=RequestContext(request, {'data1':data1, 'model1':'existe'})
	else:
		context=RequestContext(request, {'data1':data1, 'model1':model1})
	return render_to_response('deletadogr.html', context)

def succ_esta(request,form1=None,metoestass_col=None):
	monta_es=MontaEstaEspasForm(request.POST)
	monta_tp=MontaEstaTempsForm(request.POST)
	if monta_es.is_valid():
		if monta_es not in validators.EMPTY_VALUES:
			return render_to_response('errotestegr.html',{'metemp':'emptyvalues'})

def variaveis(request,empree=None):
	#ENTRA REQUEST PERMISSION AQUI- O IDEAL SERIA O DECORATOR
	if request.method=='POST':
		print 'foipost'
		mm=request.POST.copy()
		print 'request.POST.getlist[metodo]: %s'%mm.getlist('metodo')
		m=mm.getlist('metodo')
		
		print 'm: %s'%m
		b=mm.getlist('var_biodiv')
		print 'b: %s'%b;
		for i5 in b:
			print u'i5: %s'%i5
			print u'list(i5).split(','): %s'%list(i5.split(','))
			teb=testvar(list(i5.split(',')))
			if teb[0]=='erro':
				return render_to_response('erro_atributo.html',{'metemp':teb[1]})
		e=mm.getlist('var_esfor')
		print 'e: %s'%e;
		for i6 in e:
			print u'i6: %s'%i6
			print u'list(i6).split(','): %s'%list(i6.split(','))
			tee=testvar(list(i6.split(',')))
			if tee[0]=='erro':
				return render_to_response('erro_atributo.html',{'metemp':tee[1]})
		m3=[]
		for i in m:
			print 'i: %s'%i
			m4=MPP.objects.get(id=int(i))
			print m4,m4.id,i
			m4.var_biodiv=b[m.index(i)];m4.save()
			m4.var_esfor=e[m.index(i)];m4.save()
			
			#.save()
			m3.append(m4)
		return render_to_response('sucesso_atributos.html',{'metempl':m3, 'empree':empree})
	user=request.user
	empree1=Empreendimentos.objects.get(empreendimento=empree)
	if user.has_perm('alter_all_empree',empree1):
		var=[i.id for i in MetoEmprs.objects.filter(empreendimento__empreendimento=empree)]
		tbl_atributos=Atributos.objects.order_by('nome_atributo_cabecalho_coluna')
		coll_forms=[MPP2sForm(id3=ii,var_esfor=fillvar(ii, 'var_esfor')[0], var_biodiv=fillvar(ii, 'var_biodiv')[0], pae=fillvar(ii, 'var_esfor')[1],pab=fillvar(ii, 'var_biodiv')[1]) for ii in var] 
		context=RequestContext(request,{'coll_forms':coll_forms,'var':var,'tbl_atributos':tbl_atributos,'empree':empree})
		return render_to_response('variaveis.html', context)
	else:
		return render_to_response('erro_permissao.html',{'empree':empree,'user':user})

at=[i.nome_atributo_cabecalho_coluna for i in Atributos.objects.all()]
def testvar(lt):
	print lt
	m5=[]
	if lt not in validators.EMPTY_VALUES:
		for i in lt:
			if i not in at:
				m5.append(i)
		if m5 not in validators.EMPTY_VALUES:
			return ('erro',m5)
		else:
			return ('ok',[])
atenc=u'Atenção: Essas variáveis são do Padrão. Reflita sobre elas agora ou depois (voce pode mudar isso aqui quando quiser), mas antes de pactuar o formato de planilha com o Empreendedor'
cuidad=u'As variáveis do Método aqui mostrada já são do próprio Método. Não são padrões apenas. Qualquer mudança deve ser avisada ao empreendedor, de outro modo as planilhas entregues por eles não conseguirão fazer o update. Esse é um ponto crítico do sistema. Cuidado!'
def fillvar(number, var_):
	varout=MPP.objects.get(metodo=MetoEmprs.objects.get(id=number))
	if var_=='var_esfor':
		print 'varout1: %s'%varout
		if varout.var_esfor==None:
			varout=MPP.objects.get(metodo=MetoEmprs.objects.get(metogrup=MetoEmprs.objects.get(id=number).metogrup,empreendimento__empreendimento='REFERENCIA'))
			print 'varout2: %s'%varout.var_esfor
			return varout.var_esfor, atenc
			print 'varout3: %s'%varout.var_esfor
		else:
			print 'varout4: %s'%varout.var_esfor
			return varout.var_esfor, cuidad
	else:
		print 'varoutbiodiv1: %s'%varout.var_biodiv
		if varout.var_biodiv==None:
			varout=MPP.objects.get(metodo=MetoEmprs.objects.get(metogrup=MetoEmprs.objects.get(id=number).metogrup,empreendimento__empreendimento='REFERENCIA'))
			print 'varoutbiodiv2: %s'%varout.var_biodiv			
			return varout.var_biodiv, atenc
			print 'varoutbiodiv3: %s'%varout.var_biodiv
		else:
			print 'varoutbiodiv4: %s'%varout.var_biodiv			
			return varout.var_biodiv, cuidad

def montplacamp(request, empree=None):
	bio=[(i.var_biodiv,i.metodo.metogrup.metodo, i.metodo.empreendimento.empreendimento) for i in MPP.objects.filter(metodo__empreendimento__empreendimento=empree)]
	esf=[(i.var_esfor,i.metodo.metogrup.metodo, i.metodo.empreendimento.empreendimento) for i in MPP.objects.filter(metodo__empreendimento__empreendimento=empree)]
	return forcsvvar(bio,esf,empree)

def forcsvvar(bio,esf,empree):
	response=HttpResponse(mimetype='application/x-download')
	response['Content-Disposition'] = 'attachment; filename="%s.xls"'%empree
	for vari in bio:
		cabecalho=[str(vari[1].metodo).upper(),str(vari[2]).upper()]
		print 'cabecalho: %s'%cabecalho
		lfim=vari[0]
		if lfim==None:
			erro_none='acerte as variaveis de %s'%vari[1]
			return render_to_response('pego.html',{'metemp':erro_none})
		print 'lfim: %s'%lfim
		writer=csv.writer(response)
		writer.writerow([cabecalho,'BIODIV.csv'])
		writer.writerow(list(lfim.split(',')))
		for vares in esf:
			if vares[1]==vari[1]:
				cabecalho2=[str(vares[1].metodo).upper(),str(vares[2]).upper()]
				lfim2=vares[0]
				writer2=csv.writer(response)
				writer2.writerow([cabecalho2,'ESFOR.csv'])
				writer2.writerow(list(lfim2.split(',')))
	return response	

def mostraestacao(request,pk):
	estacao=MetoEstas.objects.get(id=pk)
	estref=MetoEstas.objects.get(metoempr__empreendimento__empreendimento='REFERENCIA', nome_estac=estacao.nome_estac, metoempr__metogrup=estacao.metoempr.metogrup)
#collesta=MetoEstas.objects.filter(metoempr__metogrup=estacao.metoempr.metogrup, metoempr__empreendimento__empreendimento='REFERENCIA',nome_estac=estacao.nome_estac)
	collquant=QuantApetEstas.objects.filter(metoesta=estref)
	#collmontaespa=[MontaEstaEspas.objects.filter(metoesta=i) for i in collesta]
	#collmontatemp=[MontaEstaTemps.objects.filter(metoestat=i) for i in collesta]
	return render_to_response ('estacao.html', {'estacao':estacao,'quantmetoesta':collquant})#,'montatemp':collmontatemp})



































	



#ArticleFormSet = formset_factory(ArticleForm)
