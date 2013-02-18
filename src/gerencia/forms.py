# -*- coding: utf-8 -*-
from django import forms
from models import *
from dados.models import *

class DocumentForm(forms.ModelForm):
    #docfile = forms.FileField(label='Selecione o arquivo', help_text='max. 42 megabytes')
	class Meta:
		model=Document

class DocumentZipForm(forms.ModelForm):
	class Meta:
		model=DocumentZip
		fields=('docfile',)
class MetodosadmForm(forms.Form):
	#metodoadm=forms.ChoiceField(choices=CHOICES, widget=forms.widgets.CheckboxSelectMultiple())
	metodoadm=forms.ModelMultipleChoiceField(label=u"Métodos", queryset=Metodos.objects.all(), widget=forms.widgets.CheckboxSelectMultiple)

#class EraseLevantForm(forms.Form):
#	metodo=forms.ModelMultipleChoiceField(label=u"Métodos", queryset=MPP.objects.filter(metodo__empreendimento__empreendimento='teste1'), widget=forms.widgets.CheckboxSelectMultiple)
#	campanha=forms.ModelMultipleChoiceField(label=u'Campanhas', queryset=Campanhas.objects.filter(metodo__metodo__metogrup__metodo__metodo='aves_rede',empreendimento__empreendimento='teste1'), widget=forms.widgets.CheckboxSelectMultiple)
