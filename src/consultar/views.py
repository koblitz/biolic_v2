#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from dados.forms import *
from dados.models import *
from gerencia.forms import *
from gerencia.models import *
from django.core.validators import EMPTY_VALUES
from django.core.urlresolvers import reverse
from forms import *
from django.template.loader import render_to_string
from django.utils import simplejson
import csv
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.decorators import login_required

@login_required
def consinicial(request, empree):
	context=RequestContext(request,{'empree':empree})
	return render_to_response('consultar.html',context)
@login_required
def cons_pltr(request,empree):
	espa=MontaEstaEspas.objects.filter(metoesta__metoempr__empreendimento__empreendimento=empree).order_by('metoesta','arraespaesta')
	temp=MontaEstaTemps.objects.filter(metoestat__metoempr__empreendimento__empreendimento=empree).order_by('metoestat','arratempesta')
	consulta=organizaconsulta(espa, temp, empree)
	request.session['consultare']=consulta
	context=RequestContext(request,{'consulta':consulta,'empree':empree})
	return render_to_response('planos.html',context)
#@login_required
def organizaconsulta(espa, temp, empree):
	n=0
	metlt=[]
	ltge=[]
	lt_pl_trabalho=[]
	lt_meto=[i for i in MetoEstas.objects.filter(metoempr__empreendimento__empreendimento=empree).order_by('metoempr','nome_estac')]
	for metoesta in lt_meto:
		if metoesta.nome_estac != 'estacao1':
			lt_pl_trabalho.append(metoesta.nome_estac)
		else:
			n=n+1
			lt_pl_trabalho.append(str(n)+')'+' '+str(metoesta.metoempr.metogrup)+':')
			lt_pl_trabalho.append(str(metoesta.nome_estac))
		lt_pl_trabalho.append('Espacial:')
		for monespa in espa:
			if monespa.metoesta == metoesta:
				lt_pl_trabalho.append('-->'+str(monespa.arraespaesta))
		lt_pl_trabalho.append('Temporal:')
		for montemp in temp:
			if montemp.metoestat == metoesta:
				lt_pl_trabalho.append('-->'+str(montemp.arratempesta))
	return lt_pl_trabalho
	
@login_required	
def cons_dado_levant(request,empree):
	context=RequestContext(request,{'empree':empree})
	return render_to_response('cons_dados.html',context)
@login_required
def grup_query(request, empree=None):
	dic_gru={'cl':ClassesForm,'or':OrdemsForm,'fa':FamiliasForm,'ge':GenerosForm,'im':ImprecisaosForm,'ee':Epiteto_EspecificosForm,'co':ColetorsForm}
	if request.method=='POST':
		dic_post_aux={}
		try:
			cla=request.POST.getlist('classe',None)
			if cla not in EMPTY_VALUES: dic_post_aux['classe']=cla[0]
			orde=request.POST.getlist('ordem',None)
			if orde not in EMPTY_VALUES: dic_post_aux['ordem']=orde[0]
			fam=request.POST.getlist('familia',None)
			if fam not in EMPTY_VALUES: dic_post_aux['familia']=fam[0]
			gen=request.POST.getlist('genero',None)
			if gen not in EMPTY_VALUES: dic_post_aux['genero']=gen[0]
			imp=request.POST.getlist('imprecisao',None)
			if imp not in EMPTY_VALUES: dic_post_aux['impprecisao_determinacao']=imp[0]
			epi=request.POST.getlist('epiteto_especifico',None)
			if epi not in EMPTY_VALUES: dic_post_aux['epiteto_especifico']=epi[0]
			col=request.POST.getlist('coletor',None)
			if col not in EMPTY_VALUES: dic_post_aux['coletor']=col[0]
			
			if dic_post_aux not in EMPTY_VALUES:
				print 'isso aqui veio do post dic_post_aux: %s'%len(dic_post_aux)
				lga=[(i.levantamento.id, [i,]) for i in AnimaisDados.objects.filter(eval(makeQ(dic_post_aux)))]
				print 'LGA pre if: %s'%len(lga)
				if lga not in EMPTY_VALUES:
					print 'essa é a LGA: %s'%len(lga)
					return showresult_met(lga)
					
				else:
					lgv=[(i.levantamento, i) for i in PlantasDados.objects.filter(eval(makeQ(dic_post_aux)))]
					if lgv not in EMPTY_VALUES:
						return showresult_met(lgv)
					else: return render_to_response('resultconsulta.html',{'lgg':[],'cabecalho':[],'outros':'sua consulta não retorna resultados'})
		except: pass
		if request.is_ajax():
			gru=GruposForm(request.POST).data.getlist('opcoes')
			print 'isso aqui sao os grupos pre is_valid: %s e type:%s'%(gru,type(gru))
			if gru:
				print 'isso aqui sao os grupos pos if gru: %s e type:%s'%(gru,type(gru))
				coll_form=[]
				for i5 in gru:
					coll_form.append(dic_gru[i5])
				print 'isso aqui sao os coll_form: %s'%coll_form
				context=RequestContext(request,{'coll_form':coll_form})
				html=render_to_string('grup_cons2.html',context)
				print 'o html variavel: %s'%html
    	       	res={'html':html}
    	      	return HttpResponse (simplejson.dumps(res), mimetype='application/json')
	form=GruposForm()
	context=RequestContext(request,{'form':form,'empree':empree})
	return render_to_response('grup_cons.html',context)

def makeQ(d):
	a=''
	if d not in EMPTY_VALUES:
		for key,value in d.iteritems():
			a=a+'Q('+key+'__icontains='+'\''+value+'\''+') & '
	a=a[:-3]
	return a
@login_required
def loca_query(request, empree=None):
	dic_loc={'p':ParcelasForm,'t':TrilhasForm,'m':GradesModulosForm}
	
	if request.method=='POST':
		try:
			localp=request.POST.getlist('parcela')
			if localp in EMPTY_VALUES:
				print 'parcela in EMPTY_VALUES'
				localt=request.POST.getlist('trilha')
				if localt is not None: l='t';t='5';local=localt;lo='trilha';print 'esse eh trilha: %s'%localt
			else:
				l='p';t='1';local=localp;lo='parcela';
				print 'esse eh parcela: %s'%localp
		except: pass
		if local:
			local1=dic_loc[l](request.POST)
			if local1.is_valid():
				local2=local1.cleaned_data
				print 'aqui eh o local2:%s'%local2
			lgg=[]
			for i in local2[lo]:
				llev=[i2 for i2 in Levantamentos.objects.filter(tipo_ua=t,id_ua=i.id)]
				for ii in llev:
					lg=[]
					try:
						lg=[i3 for i3 in AnimaisDados.objects.filter(levantamento=ii)]
					except: pass
					if lg in EMPTY_VALUES:
						try:
							lg=[i3 for i3 in PlantasDados.objects.filter(levantamento=ii)]
						except: pass
					if lg in EMPTY_VALUES:
						try:
							lg=[i3 for i3 in AbioticosDados.objects.filter(levantamento=ii)]
						except: pass
					lgg.append((ii.id,lg))
			if lgg not in EMPTY_VALUES:
				return showresult_met(lgg)
			else: return render_to_response('resultconsulta.html',{'lgg':[],'cabecalho':[]})
			#return showresult_met(lgg)
		if request.is_ajax():
			loc=LocalidadesForm(request.POST).data
			if loc:
				print 'isso aqui eh o local %s'%loc
				form=dic_loc[loc['localidade']]
				context=RequestContext(request,{'form2':form})
				html=render_to_string('loca_cons2.html',context)
            	res={'html':html}
            	return HttpResponse (simplejson.dumps(res), mimetype='application/json')
	form=LocalidadesForm()
	context=RequestContext(request,{'form':form,'empree':empree})
	return render_to_response('loca_cons.html',context)

@login_required
def meto_query(request, empree=None):
	if request.method=='POST':
		try:
			dados=request.POST.getlist('num_campanha',None)
		except: pass
		print 'isso aqui eh a dados %s'%dados
		if dados:
			lgg=[]
			for i in dados:
				if i not in EMPTY_VALUES:
					llev=[i for i in Levantamentos.objects.filter(campanha=i)]
					for ii in llev:
						lg=[]
						try:
							lg=[i3 for i3 in AnimaisDados.objects.filter(levantamento=ii)]
						except: pass
						if lg in EMPTY_VALUES:
							try:
								lg=[i3 for i3 in PlantasDados.objects.filter(levantamento=ii)]
							except: pass
						if lg in EMPTY_VALUES:
							try:
								lg=[i3 for i3 in AbioticosDados.objects.filter(levantamento=ii)]
							except: pass
						lgg.append((ii.id,lg))			
			if lgg not in EMPTY_VALUES:
				return showresult_met(lgg)
			else:
				return HttpResponseRedirect(reverse('consultar:forcsv2', kwargs={'nomecsv':'sem_lev'}))#render_to_response('resultconsulta.html',{'lgg':[],'cabecalho':[], 'codcabeca':'})
		if request.is_ajax():
			try:
				campa=request.POST.getlist('metodo',None)
			except: pass
			print 'isso aqui eh a campa pre if %s'%campa
			if campa:
				print 'isso aqui eh a campa %s'%campa
				campa1=int(campa[0])
				print 'isso aqui eh a campa1 %s'%campa1
				form=Campanhas3Form(campa1)
				context=RequestContext(request,{'form2':form})
				html=render_to_string('meto_camp_cons2.html',context)
            	res={'html':html}
            	return HttpResponse (simplejson.dumps(res), mimetype='application/json')
	form=Campanhas1Form(empree)
	context=RequestContext(request,{'form':form,'empree':empree})
	return render_to_response('meto_camp_cons.html',context)

dil={'1':Parcelas,'5':Trilhas}
def showresult_met(lgg):
	lfim=[];lfim1=[]
	print 'in showresult'
	print 'lgg:%s'%len(lgg)
	#lgg=[i for i in lgg if type(i)!=str]
	for i in lgg:
		print u'i eh %s:'%str(smart_str(i))
		lev=Levantamentos.objects.get(id=i[0])
		#print 'lev eh %s:'%len(lev)
		local=dil[lev.tipo_ua].objects.get(id=lev.id_ua)
		if lev.tipo_ua=='1':
			print 'if lev.tipo_ua==\'1\''
			print 'type de i[1]: %s'%type(i[1])
			for ii in i[1]:
				lp=[]
				lp.append((local.trilha.grade_modulo.abrev,local.trilha.nome,local.nome,lev.metodo.metodo.metogrup.metodo.metodo,lev.campanha.num_campanha,
lev.dt_inicial.isoformat(),lev.dt_final.isoformat(),ii.genero,ii.imprecisao_determinacao,ii.epiteto_especifico,ii.numero_coleta,ii.lote_individuo,AnimaisVarchar.objects.get(atributo=5, animais_dado=ii.id).valor,AnimaisVarchar.objects.get(atributo=6, animais_dado=ii.id).valor,ii.coletor))
				lfim1.append(lp)
				lfim.append(list(lp[0]))
				print 'len lp: %s '%len(lp)
				print 'len lp[0]: %s '%len(lp[0])
				print 'len lfim: %s '%len(lfim)
				global lfim
			cabecalho=cabecalhof('p')
		if lev.tipo_ua=='5':
			print 'if lev.tipo_ua==\'5\''
			for ii in i[1]:
				lp=[]
				lp.append((local.trilha.grade_modulo.abrev,local.nome,lev.metodo.metodo.metogrup.metodo.metodo,lev.campanha.num_campanha,
lev.dt_inicial.isoformat(),lev.dt_final.isoformat(),ii.genero,ii.imprecisao_determinacao,ii.epiteto_especifico,ii.numero_coleta,ii.lote_individuo,AnimaisVarchar.objects.get(atributo=5, animais_dado=ii.id).valor,AnimaisVarchar.objects.get(atributo=6, animais_dado=ii.id).valor,ii.coletor))
				lfim1.append(lp)
				lfim.append(list(lp[0]))
				print 'trilha--len lp: %s '%len(lp)
				print 'trilha--len lp[0]: %s '%len(lp[0])
				print 'trilha--len lfim: %s '%len(lfim)
			cabecalho=cabecalhof('t')
	#request.session['ltdadosbio']=ltfim
	return render_to_response('resultconsulta.html',{'lgg':lfim1,'cabecalho':cabecalho[0], 'codcabeca':cabecalho[1]})
def cabecalhof(pt):
	if pt=='p':
		return (['grade_modulo','trilha','parcela','metodo','campanha','dt_inicial','dt_final','genero','imprecisao_determinacao','epiteto_especifico','numero_coleta','lote_individuo','n_tombamento', 'nome_intituicao','coletor'],'p')
	elif pt=='t':
		return (['grade_modulo','trilha','metodo','campanha','dt_inicial','dt_final','genero','imprecisao_determinacao','epiteto_especifico','numero_coleta','lote_individuo','n_tombamento', 'nome_intituicao','coletor'], 't')

def forcsv(request, nomecsv=None, codcabeca=None):
	consulta=request.session.get('consultare')
	if consulta:
		lt_pl_trabalho=consulta
	print 'consulta: %s'%consulta
	
	#global lfim
	response = HttpResponse(mimetype='text/csv')
	if nomecsv=='dados_bioticos':
		ltfim=request.session.get('ltdadosbio')
		response['Content-Disposition'] = 'attachment; filename="%s.csv"'%nomecsv
		writer=csv.writer(response)
		print 'em forcsv: %s'%nomecsv
		writer.writerow(cabecalhof(codcabeca)[0])
		for i in lfim:
			try:
				i=eval(i)
			except:pass
			writer.writerow(i)
		return response

	elif nomecsv=='tbl_atributos':
		response['Content-Disposition'] = 'attachment; filename="%s.csv"'%nomecsv
		cabecalho1=['Tipo_Valor: 1-Date, 2-Float, 3-Varchar, 4-Integer, 5-Time, 6-Text']
		cabecalho11=['Grupo: 1-Animal, 2-Vegetal, 3-Abiotico']
		cabecalho=['Atributos a serem usados:']
		cabecalho2=[u'nome', u'descricao', u'legenda', u'tipo_valor', u'grupo', u'unidade_utilizada']
		lfim=[[i[1].nome_atributo_cabecalho_coluna,i[1].descricao,i[1].legenda,i[1].tipo_valor,i[1].referencia,i[1].unidade_utilizada] for i in enumerate(Atributos.objects.order_by('nome_atributo_cabecalho_coluna'))]
		writer=csv.writer(response)
		writer.writerow(cabecalho1);writer.writerow(cabecalho11);writer.writerow(cabecalho);writer.writerow(cabecalho2)
		[writer.writerow([ii.encode('utf-8') for ii in i]) for i in lfim]
		return response
	elif nomecsv=='plano_trabalho':
		response['Content-Disposition'] = 'attachment; filename="%s.csv"'%nomecsv
		cabecalho=''
		lfim=lt_pl_trabalho
		writer=csv.writer(response)
		writer.writerow(cabecalho)
		[writer.writerow([i]) for i in lfim]
#		for i in lfim:
#			try:
#				i=eval(i)
#			except:pass
#			writer.writerow(i)
		return response
	elif nomecsv=='sem_lev':
		return render_to_response('resultconsulta.html',{'outros':u'Campanha cadastrada, mas sem levantamentos'})

def r_e(lst):
	if type(lst)==list:
		try:
			if len(lst) == 1:
				return lst
			else:
				return [r_e(i) for i in lst]
		except:pass #TypeError:.encode("utf-8")
		return lst
	else:
		return lst	







	
