from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
#from usuarios.models import Usuarios

class RegistrationForm(UserCreationForm):
	pass
#	username=forms.CharField(label=(u'User Name'))
#	email=forms.EmailField(label=(u'email'))
#	password=forms.CharField(label=(u'Senha'), widget=forms.PasswordInput(render_value=False))
#	class Meta:
#		model=User
#		exclude=('user',)
#	def clean_username(self):
#		username=self.cleaned_data['username']
#		try:
#			User.objects.get(username=username)
#		except Usuarios.DoesNotExist:
#			return username
#		raise forms.ValidationError('Esse usuario existe, escolha outro')
#	def is_authenticated(self):
#		return False
