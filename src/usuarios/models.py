from django.contrib.auth.models import User
from dados.models import Empreendimentos
from django.db.models.signals import post_save
from django.db import models 

#class Usuarios(models.Model):
#	user=models.OneToOneField(User)
#	def is_authenticated(self):
#		return False
#	def __unicode__(self):
#		return self.user
#def create_user_profile(sender,instance,created,**kwargs):
#	if created:
#		usuarios,new=Usuarios.objects.get_or_create(user=instance)

#post_save.connect(create_user_profile,sender=User)
