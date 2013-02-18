from django.db import models
from dados.models import Empreendimentos

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    def __unicode__(self):
        return self.docfile.name

class DocumentZip(models.Model):
#	def __init__(self):
	#	self=self
#		filename=filename	
#		instance=instance
#		return 'empreendimentos'

	docfile = models.FileField(upload_to='empreendimentos')
	empreendimento=models.ForeignKey(Empreendimentos, blank=True, null=True)
	def __unicode__(self):
		return u'%s'%(self.docfile.name)

class CabecalhosLocais(models.Model):
	modelo=models.CharField(max_length=100, unique=True)
	lista_campo=models.TextField()
	def __unicode__(self):
		return u'%s-%s'%(self.modelo,self.lista_campo)

