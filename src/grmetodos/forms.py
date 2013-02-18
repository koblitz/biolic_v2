#-*- coding: utf-8 -*-
from django import forms
from django.forms import CheckboxSelectMultiple
from django.db import models
from dados.models import MPP,MetoEmprs,QuantApetEstas, MetoEstas, Apetrechos, QuantApetEstas,ArraEspaEstas,ArraTempEstas,MontaEstaEspas,MontaEstaTemps
from django.utils.safestring import mark_safe
from django.forms.formsets import BaseFormSet
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.models import inlineformset_factory
class MetodosadmForm(forms.Form):
	#metodoadm=forms.ChoiceField(choices=CHOICES, widget=forms.widgets.CheckboxSelectMultiple())
	metodoadm=forms.ModelMultipleChoiceField(label=u"Métodos", queryset=MPP.objects.filter(metodo__empreendimento__empreendimento__iexact='referencia'), widget=forms.widgets.CheckboxSelectMultiple)#RadioSelect)

class Metodosadm1Form(forms.Form):
	metodoadm1=forms.ModelMultipleChoiceField(label=u"Métodos", queryset=None, widget=forms.widgets.RadioSelect)
	def __init__(self,empree,*args,**kwargs):
		super(Metodosadm1Form,self).__init__(*args,**kwargs)
		self.fields['metodoadm1'].queryset=MetoEmprs.objects.filter(empreendimento__empreendimento=empree)

class MPP1sForm(forms.ModelForm):
	var_biodiv=forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':40}))
	var_esfor=forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
	class Meta:
		model=MPP

class MPP2sForm(forms.Form):
	metodo=forms.ModelChoiceField(label=u"Métodos", queryset=None)
	var_biodiv=forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':40}))
	var_esfor=forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
	def __init__(self,id3=None,var_esfor=None,var_biodiv=None,pae=None,pab=None,*args,**kwargs):
		super(MPP2sForm,self).__init__(*args,**kwargs)
		self.fields['metodo'].queryset=MPP.objects.filter(metodo=MetoEmprs.objects.get(id=id3))
		self.fields['metodo'].empty_label=None
		self.fields['var_esfor'].initial=var_esfor
		self.fields['var_biodiv'].initial=var_biodiv
		self.fields['var_biodiv'].help_text='%s'%pab
		self.fields['var_esfor'].help_text='%s'%pae
		
class Campanhas3Form(forms.Form):
	num_campanha=forms.ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	def __init__(self,metodo,*args,**kwargs):
		super(Campanhas3Form,self).__init__(*args,**kwargs)
		self.fields['num_campanha'].queryset=Campanhas.objects.filter(metodo=metodo)

class MPPsForm(forms.ModelForm):
	def __init__(self,idd=None,*args,**kwargs):
		super(MPPsForm, self).__init__(*args,**kwargs)
		self.fields['metodo'].queryset=MPP.objects.get(metodo=MetoEmprs.objects.get(id=idd.id))
	class Meta:
		model=MPP

class QuantApetMetoEstasForm(forms.Form):
	class MyModelChoiceField(forms.ModelChoiceField):
		def label_from_instance(self,obj):
			return u'estacao'#%obj.nome_estac
	metoesta_ref=MyModelChoiceField(empty_label=None,queryset=None,widget=forms.CheckboxSelectMultiple)
	
	def __init__(self,idd,*args,**kwargs):
		super(QuantApetMetoEstasForm,self).__init__(*args,**kwargs)
		self.fields['metoesta_ref'].queryset=MetoEstas.objects.filter(id=idd)
		self.fields['metoesta_ref'].label=''
		a=''
		for i in QuantApetEstas.objects.filter(metoesta=MetoEstas.objects.get(id=idd)):
			a=a+str(i.quantidade)+' de '+str(i.apettipo.quanttipoapet)+'<b>'+str(i.apettipo.apetrecho)+'</b>'+'<p>'
		self.fields['metoesta_ref'].help_text=mark_safe(a)

class QuantApetEstas1Form(forms.Form):
	metoesta=forms.ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	def __init__(self,metoempr,*args,**kwargs):
		super(QuantApetEstas1Form,self).__init__(*args,**kwargs)
		self.fields['metoesta'].queryset=MetoEstas.objects.filter(metoempr=metoempr)

class ArraEspaEstaForm(forms.Form):
	arraestaespaform=forms.ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	def __init__(self,listid,*args,**kwargs):
		super(ArraEspaEstaForm,self).__init__(*args,**kwargs)
		self.fields['arraestaespaform'].queryset=ArraEspaEstas.objects.filter(pk__in=listid)
		self.fields['arraestaespaform'].label=''

class ArraTempEstaForm(forms.Form):
	arraestatempform=forms.ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	#estacao=models.CharField(max_leght='21')#ModelChoiceField(queryset=None, empty_label=None,widget=forms.CheckboxSelectMultiple())
	def __init__(self,listid,*args,**kwargs):
		super(ArraTempEstaForm,self).__init__(*args,**kwargs)
		self.fields['arraestatempform'].queryset=ArraTempEstas.objects.filter(pk__in=listid)
		self.fields['arraestatempform'].label=''
	#	self.fields['estaco'].label='estacao'

class MetaMontaESForm(forms.ModelForm):
	arraespaesta=forms.ModelChoiceField(queryset=None, empty_label=None)
	metoesta=forms.ModelChoiceField(queryset=None, empty_label=None)
	class Meta:
		model=MontaEstaEspas
	def __init__(self,*args,**kwargs):
		ltesf=kwargs.pop('ltesf')
		metolt=kwargs.pop('metolt')
		super(MetaMontaESForm, self).__init__(*args,**kwargs)
		self.fields['arraespaesta'].widget=forms.CheckboxSelectMultiple()
		self.fields['arraespaesta'].queryset=ArraEspaEstas.objects.filter(pk__in=ltesf)
		self.fields['metoesta'].queryset=MetoEstas.objects.filter(pk__in=metolt)
		

class MetaMontaFSForm(forms.ModelForm):
	arratempesta=forms.ModelChoiceField(queryset=None, empty_label=None)
	metoestat=forms.ModelChoiceField(queryset=None, empty_label=None)
	class Meta:
		model=MontaEstaTemps
	def __init__(self,*args,**kwargs):
		listlt=kwargs.pop('listlt')
		metolt=kwargs.pop('metolt')
		super(MetaMontaFSForm, self).__init__(*args,**kwargs)
		self.fields['arratempesta'].widget=forms.CheckboxSelectMultiple()
		self.fields['arratempesta'].queryset=ArraTempEstas.objects.filter(pk__in=listlt)
		self.fields['metoestat'].queryset=MetoEstas.objects.filter(pk__in=metolt)



