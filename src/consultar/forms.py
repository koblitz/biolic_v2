# -*- coding: utf-8 -*-
from django import forms
from models import *
from dados.models import *


class CampanhasForm(forms.ModelForm):
	num_campanha=forms.ModelMultipleChoiceField(queryset=Campanhas.objects.all(),required=False, widget=forms.CheckboxSelectMultiple,label='Campanhas')
	class Meta:
		model=Campanhas
		exclude=('empreendimento','pessoa','descricao','dt_inicio','dt_fim',
'precip_periodo','temp_periodo','pessoa2','num_campanha')
class Campanhas1Form(forms.ModelForm):
	def __init__(self,empree=None,*args,**kwargs):
		super(Campanhas1Form,self).__init__(*args,**kwargs)
		self.fields['metodo'].queryset=MPP.objects.filter(metodo__empreendimento__empreendimento=empree)
	class Meta:
		model=Campanhas
		exclude=('empreendimento','pessoa','descricao','dt_inicio','dt_fim','precip_periodo','temp_periodo','pessoa2','num_campanha')

#class Campanhas1Form(forms.ModelForm):
#	class Meta:
#		model=Campanhas
#		exclude=('empreendimento','pessoa','descricao','dt_inicio','dt_fim','precip_periodo','temp_periodo','pessoa2','num_campanha')

class Campanhas3Form(forms.Form):
	num_campanha=forms.ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	def __init__(self,metodo,*args,**kwargs):
		super(Campanhas3Form,self).__init__(*args,**kwargs)
		self.fields['num_campanha'].queryset=Campanhas.objects.filter(metodo=metodo)

class LocalidadesForm(forms.Form):
	CHOICE=[('t','Trilhas'),('p','Parcelas')]
	localidade=forms.ChoiceField(required=False, widget=forms.RadioSelect(),choices=CHOICE)

class GruposForm(forms.Form):
	CHOICE=[('cl','Classe'),('or','Ordem'),('fa','Familia'),('ge','Genero'),('im','Imprecisao'),('ee','Epiteto_Especifico'),('co','Coletor')]
	opcoes=forms.ChoiceField(required=False, widget=forms.CheckboxSelectMultiple,label='Opções de Pesquisa',choices=CHOICE)

class ClassesForm(forms.Form):
	classe = forms.CharField(widget=forms.TextInput)
class OrdemsForm(forms.Form):
	ordem = forms.CharField(widget=forms.TextInput)
class FamiliasForm(forms.Form):
	familia = forms.CharField(widget=forms.TextInput)
class GenerosForm(forms.Form):
	genero = forms.CharField(widget=forms.TextInput)
class ImprecisaosForm(forms.Form):
	imprecisao = forms.CharField(widget=forms.TextInput)
class Epiteto_EspecificosForm(forms.Form):
	epiteto_especifico = forms.CharField(widget=forms.TextInput)
class ColetorsForm:
	coletor = forms.CharField(widget=forms.TextInput)

class GradesModulosForm(forms.ModelForm):
	gradesmodulo=forms.ModelMultipleChoiceField(queryset=GradesModulos.objects.all(),required=False, widget=forms.CheckboxSelectMultiple,label='Modulos')
	class Meta:
		model=GradesModulos
		exclude=('nome','pessoa','empreendimento','tipo','qnt_trilhas','abrev')

class TrilhasForm(forms.ModelForm):
	trilha=forms.ModelMultipleChoiceField(queryset=Trilhas.objects.all(),required=False, widget=forms.CheckboxSelectMultiple,label='Trilhas')
	class Meta:
		model=Trilhas
		exclude=('grade_modulo','topografia','inclinacao','coordenada','comp','rapeld','nome')

class ParcelasForm(forms.ModelForm):
	parcela=forms.ModelMultipleChoiceField(queryset=Parcelas.objects.all(),required=False, widget=forms.CheckboxSelectMultiple,label='Parcelas')
	class Meta:
		model=Parcelas
		exclude=('trilha','nome','topografia','inclinacao','coordenada','dist_paralela_trilha','dist_perpend_trilha','segue_curva_nivel','comprimento','obs')
