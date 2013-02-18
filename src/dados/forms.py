# -*- coding: utf-8 -*-
from django import forms
from models import *
from django import forms
from dados.models import *
from django.db.models import Q

class Empreendimentos1Form(forms.Form):
	empreendimento=forms.ModelChoiceField(label='Empreendimentos', queryset=None, empty_label=None)
	def __init__(self, user=None, *args, **kwargs):
		super(Empreendimentos1Form, self).__init__(*args,**kwargs)
		self.fields['empreendimento'].queryset=Empreendimentos.objects.filter(created_by=str(user)).exclude(empreendimento='REFERENCIA')

class EmpreendimentosForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EmpreendimentosForm, self).__init__(*args,**kwargs)
		#self.fields['created_by'].queryset=User.objects.filter(id=userid)
		self.fields['created_by'].widget=forms.HiddenInput()
	class Meta:
		model=Empreendimentos

class EmpresasForm(forms.ModelForm):
	class Meta:
		model=Empresas

class PessoasForm(forms.ModelForm):
	class Meta:
		model=Pessoas

class AtriEspasForm(forms.ModelForm):

    class Meta:
        model=AtriEspas

class UnidEspasForm(forms.ModelForm):
    class Meta:
        model=UnidEspas

class AtriUnidEspasForm(forms.ModelForm):
	class Meta:
		model=AtriUnidEspas

class ArraEspasForm(forms.ModelForm):

    class Meta:
        model=ArraEspas

class ArraEspaEstasForm(forms.ModelForm):
    class Meta:
        model=ArraEspaEstas

class ApetrechosForm(forms.ModelForm):
    class Meta:
        model=Apetrechos

class TipoEsfoEspasForm(forms.ModelForm):
    class Meta:
        model=TipoEsfoEspas

class ApetTiposForm(forms.ModelForm):
    class Meta:
        model=ApetTipos

class MetodosForm(forms.ModelForm):
    class Meta:
        model=Metodos

class GrupoBioticosForm(forms.ModelForm):
    class Meta:
        model=GrupoBioticos

class MetoGrupsForm(forms.ModelForm):
    class Meta:
        model=MetoGrups
class MetoEmprsForm(forms.ModelForm):
    class Meta:
        model=MetoEmprs

class MetoEstasForm(forms.ModelForm):
    class Meta:
        model=MetoEstas

class QuantApetEstasForm(forms.ModelForm):
    class Meta:
        model=QuantApetEstas

class ArraTempsForm(forms.ModelForm):
    class Meta:
        model=ArraTemps


class UnidTempsForm(forms.ModelForm):
    class Meta:
        model=UnidTemps

class ArraTempEstasForm(forms.ModelForm):
    class Meta:
        model=ArraTempEstas

class MontaEstaTempsForm(forms.ModelForm):
	def __init__(self,metodo=None,metoempr=None,*args,**kwargs):
		super(MontaEstaTempsForm, self).__init__(*args,**kwargs)
		if metodo:
			self.fields['metoestat'].empty_label=None			
			self.fields['metoestat'].queryset=MetoEstas.objects.filter(metoempr=metoempr)
			self.fields['metoestat'].label='Estação'
			self.fields['arratempesta'].empty_label=None
			self.fields['arratempesta'].widget=forms.CheckboxSelectMultiple()
			self.fields['arratempesta'].queryset=ArraTempEstas.objects.filter	(id__in=MontaEstaTemps.objects.values_list('arratempesta').filter(Q(metoestat__metoempr__empreendimento__empreendimento__icontains='REFERENCIA'),Q(metoestat__metoempr__metogrup__metodo__metodo__icontains=metodo)))
	class Meta:
		model=MontaEstaTemps

class MontaEstaEspasForm(forms.ModelForm):
	def __init__(self, metodo=None, metoempr=None, *args, **kwargs):
		super(MontaEstaEspasForm, self).__init__(*args,**kwargs)
		if metodo:
			self.fields['metoesta'].empty_label=None
			self.fields['metoesta'].queryset=MetoEstas.objects.filter(metoempr=metoempr)
			self.fields['metoesta'].label='Estação'
			self.fields['arraespaesta'].empty_label=None
			self.fields['arraespaesta'].widget=forms.CheckboxSelectMultiple()
			self.fields['arraespaesta'].queryset=ArraEspaEstas.objects.filter	(id__in=MontaEstaEspas.objects.values_list('arraespaesta').filter(Q(metoesta__metoempr__empreendimento__empreendimento__icontains='REFERENCIA'),Q(metoesta__metoempr__metogrup__metodo__metodo__icontains=metodo)))
	class Meta:
		model=MontaEstaEspas




