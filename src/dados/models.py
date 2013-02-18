#-*- coding: utf-8 -*-
from django.db import models
from django.core import validators
from django.contrib.auth.models import User

def tira(stri):
	if 'de None de' in stri: stri=stri.replace('de None de','')
	if 'None de' in stri: stri=stri.replace('None de','')
	if 'de None -' in stri: stri=stri.replace('de None -','')
	if 'de None' in stri: stri=stri.replace('de None','')
	if '- None' in stri: stri=stri.replace('- None','')
	if ', None' in stri: stri=stri.replace(', None','')
	if ' None' in stri: stri=stri.replace(' None','')
	if 'None' in stri: stri=stri.replace('None','')
	if 'Non' in stri: stri=stri.replace('Non','')
	return stri

	

class Empreendimentos(models.Model):
	empreendimento=models.CharField(max_length=100, unique=True)
	cnpj=models.CharField(max_length=100,blank=True, null=True)
	mail_resp=models.EmailField(max_length=100, blank=True, null=True)
	created_by=models.ForeignKey(User, blank=True, null=True)
	outro_mail=models.EmailField(max_length=100, blank=True, null=True)
	
	class Meta:
		db_table='tbl_empreendimentos'
	def __unicode__(self):
		return self.empreendimento

class Empresas(models.Model):
	empresa=models.CharField(max_length=100, unique=True)
	empreendimento=models.ForeignKey(Empreendimentos,blank=True, null=True)
	cnpj=models.CharField(max_length=100, blank=True, null=True)
	mail_resp=models.EmailField(max_length=100, blank=True, null=True)
	outro_mail=models.EmailField(max_length=100, blank=True, null=True)
	class Meta:
		db_table='tbl_empresas'
		unique_together=('empresa','empreendimento')
	def __unicode__(self):
		return self.empresa

class Pessoas(models.Model):
	pessoa=models.CharField(max_length=100, unique=True)
	empreendimento=models.ForeignKey(Empreendimentos,blank=True, null=True)
	cnpj=models.CharField(max_length=100, null=True, blank=True)
	mail=models.EmailField(max_length=100, null=True, blank=True)
	outro_mail=models.EmailField(max_length=100, null=True, blank=True)
	class Meta:
		db_table='tbl_pessoas'
	
	def __unicode__(self):
		return self.pessoa

class AtriEspas(models.Model):#1
	''' define os simples atributos que podem ser usados no banco, para associar a unidade. Ex: distancia, altura...'''
	atriespa=models.CharField(max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True,  null=True)

	class Meta:
		db_table='tbl_atributos_espacias'
		ordering=('atriespa',)
	def __unicode__(self):
		return self.atriespa

class UnidEspas(models.Model):#2
	''' define as unidades espaciais. Ex: metro, metro cubico... '''
	unidespa=models.CharField(max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True,  null=True)

	class Meta:
		db_table='tbl_unidades_espaciais'
		ordering=('unidespa',)
	def __unicode__(self):
		return self.unidespa

class AtriUnidEspas(models.Model):#3
	''' associa o atributo a unidade. Aqui é onde será feita a escolha de mensuracão
de distancia em metros, altura em centímetros...'''
	atriespa=models.ForeignKey(AtriEspas)
	unidespa=models.ForeignKey(UnidEspas, verbose_name=u'unidade espacial')

	class Meta:
		db_table='tbl_atributos_unidades_espaciais'
		unique_together=('atriespa','unidespa')
		ordering=('unidespa', 'atriespa')
	def __unicode__(self):
		return tira(u'%s de %s' %(self.unidespa, self.atriespa))

class ArraEspas(models.Model):#4
	''' define os tipos de arranjos espaciais que poderão ser usados no banco '''
	arraespa=models.CharField(u'arranjo espacial', max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True,  null=True)

	class Meta:
		db_table='tbl_arranjos_espaciais'
		ordering=['arraespa',]
	def __unicode__(self):
		return self.descricao

class ArraEspaEstas(models.Model):#5 pensar em colocar um booleano
#que indique que o quantidade é variável ou médio
	''' indica como o arranjo espacial será mensurado. Ex: arranjo - entre apetrehos, atributos com unidades - distancia em metros, medida - 10. Se a medida precisa for alguma string, então o campo medida fica nulo e se coloca isso em outra descricoes)'''
	arraespa=models.ForeignKey(ArraEspas, verbose_name=u'arranjo espacial')
	atriunidespa=models.ForeignKey(AtriUnidEspas, verbose_name=u'atributos/unidades', blank=True,  null=True)
	quantidade=models.FloatField(verbose_name=u'medida do quantitativo do arranjo', blank=True, null=True)
	maisoumenos=models.NullBooleanField(u'médios?', default=0, blank=False, choices=((1,'sim'),(0,'não')))
	outra_descricao=models.TextField(u'outra medida do arranjo espacial', blank=True, null=True)

	class Meta:
		db_table='tbl_arranjos_espaciais_estacoes'
		ordering=['arraespa','atriunidespa']
	def __unicode__(self):
		if self.arraespa not in validators.EMPTY_VALUES:
			if 'numero de estacoes por unidade amostral' in str(self.arraespa):
				return tira(u'%s: %.1f'%(self.arraespa, self.quantidade))
		if self.maisoumenos==1:
			return tira(u'%s, com %.1f %s médios'%(self.arraespa, self.quantidade, self.atriunidespa))
		elif self.atriunidespa is not None and self.quantidade is not None and self.outra_descricao != '':
			return tira(u'%s, com %.1f %s, sendo %s'%(self.arraespa, self.quantidade, self.atriunidespa, self.outra_descricao))
		elif self.atriunidespa is None and self.quantidade is None and self.outra_descricao == '':
			return tira(u'%s')%self.arraespa
		elif self.outra_descricao == '':
			return tira(u'%s, com %.1f %s, '%(self.arraespa, self.quantidade, self.atriunidespa))
		else:
			return tira(u'%s, medida %s, como %s'%(self.arraespa, self.atriunidespa, self.outra_descricao))


class Apetrechos(models.Model):#6
	''' define os apetrechos apetrechos que poderão ser usados no banco '''
	apetrecho=models.CharField(max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True,  null=True)

	class Meta:
		db_table='tbl_apetrechos'
		ordering=['apetrecho',]
	def __unicode__(self):
		return self.apetrecho

class TipoEsfoEspas(models.Model):#7
	''' define o tipo de esforco espacial.
Por exemplo: Peneirada, Tarrafada, Passagem... '''
	tipoesfoespa=models.CharField(u'tipo de esforço espacial', max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True, null=True)

	class Meta:
		db_table='tbl_tipo_esforcos_espaciais'

	def __unicode__(self):
		return self.tipoesfoespa

class QuantTipoApets(models.Model):#8
	'''Caso haja o Tipo de Esforco Espacial TipoEsfoEspas, essa classe define a quantidade em que esta esta estabelecida. Defaul 1'''
	tipoesfoespa=models.ForeignKey(TipoEsfoEspas, null=True, blank=True)	
	quantidade=models.FloatField(default=1)
	class Meta:
		db_table='tbl_quantidade_tipos_apetrechos'
		unique_together=('tipoesfoespa','quantidade')
	def __unicode__(self):
		if self.quantidade==1:
			return tira('%s %s'%(self.quantidade, str(self.tipoesfoespa)[:-1]))
		return tira('%s %s'%(self.quantidade, self.tipoesfoespa))

class ApetDefis	(models.Model):#8-1
	'''Define o apetrecho quanto as suas dimensões espaciais'''
	apetrecho=models.ForeignKey(Apetrechos)
	atriunidespa=models.ForeignKey(AtriUnidEspas, null=True, blank=True)
	valor=models.FloatField(null=True,blank=True)
	outras_caracteristicas=models.TextField(null=True,blank=True)
	class Meta:
		db_table='apetrecho_definidos'
		unique_together=('apetrecho','atriunidespa')
		ordering=['apetrecho','valor','atriunidespa']
	def __unicode__(self):
#		return u'%s'%self.apetrecho
		if self.outras_caracteristicas in validators.EMPTY_VALUES:
			return tira(u'%s de %s - %s'%(self.apetrecho, self.valor, self.atriunidespa))
		else:
			return tira(u'%s %s %s %s'%(self.apetrecho, self.valor, self.atriunidespa, self.outras_caracteristicas))

class ApetTipos(models.Model):#8-2
	''' Indica a quantidade de tipo de esforco espacial será empregado
#por apetrecho. Por exmeplo: apetrecho - tarrafa(de largura XX e altura XX), esforco - tarrafada, quantidade -1'''
	apetrecho=models.ForeignKey(Apetrechos)
	quanttipoapet=models.ForeignKey(QuantTipoApets, default=11)
	class Meta:
		db_table='tbl_apetrecho_tipo_esforcos_espaciais'
		unique_together=('apetrecho','quanttipoapet')
		ordering=['apetrecho','quanttipoapet']
	def __unicode__(self):
		if self.quanttipoapet in validators.EMPTY_VALUES:
			return tira(u'%s' %(self.apetrecho))
		else:
			return tira(u'%s %s' %(self.quanttipoapet, self.apetrecho))

class Metodos(models.Model):#9
	''' define os métodos que serão usados no banco '''
	metodo=models.CharField(u'método', max_length=100, unique=True)
	descricao=models.TextField(u'descrição')
	class Meta:
		db_table='tbl_metodos'
		ordering=['metodo',]
	def __unicode__ (self):
		if self.descricao !='':
			return u'%s'%self.descricao
		else:
			return u'%s'%self.metodo

class GrupoBioticos(models.Model):#10
	''' define os grupos bióticos que serão
	utilizados no banco '''
	grupobiotico=models.CharField(u'grupo', max_length=100, unique=True)
	descricao=models.TextField(u'descrição')
	class Meta:
		db_table='tbl_grupo_bioticos'

	def __unicode__ (self):
		if self.descricao !='':
			return u'%s'%self.descricao
		else:
			return u'%s'%self.grupobiotico
		return self.grupobiotico

class MetoGrups(models.Model):#11
	metodo=models.ForeignKey(Metodos)
	grupobiotico=models.ForeignKey(GrupoBioticos)
	class Meta:
		db_table='tbl_metodos_gruposbioticos'
		unique_together=('metodo','grupobiotico')
	def __unicode__ (self):
		return u'%s para %s'%(self.metodo, self.grupobiotico)

class MetoEmprs(models.Model):#12
	metogrup=models.ForeignKey(MetoGrups)
	empreendimento=models.ForeignKey(Empreendimentos)
	class Meta:
		db_table='tbl_metodos_empreendimentos'
		unique_together=('metogrup','empreendimento')
	def __unicode__ (self):
		return u'%s de %s'%(self.metogrup, self.empreendimento)

class MetoEstas(models.Model):#13
	metoempr=models.ForeignKey(MetoEmprs)
	nome_estac=models.CharField(max_length=100)
	class Meta:
		db_table='tbl_metodos_empreendimento_estacoes'
		unique_together=('metoempr','nome_estac')
		ordering=['metoempr','nome_estac']
	def __unicode__ (self):
		return u'%s, %s'%(self.metoempr, self.nome_estac)

#class QuantApetEstasManager(models.Manager):
#	def __unicode__(self):
#		return u'%s'%self.metoesta.nome_estac


class QuantApetEstas(models.Model):#14
	''' Indica a quantidade de vezes que o apetrecho (já dada a quantidade do esforco espacial por apetrecho) é utilizada em uma estaćão'''
	apettipo=models.ForeignKey(ApetTipos, verbose_name=u'apetrecho')
	metoesta=models.ForeignKey(MetoEstas)
	quantidade=models.FloatField(default=1)
#	objects=models.Manager()
#	objects_forms=QuantApetEstasManager()
	class Meta:
		db_table='tbl_quantidade_apetrechos_estacoes'
		unique_together=('apettipo','metoesta','quantidade')
		ordering=['metoesta', 'apettipo', 'quantidade']
	def __unicode__(self):
		if self.quantidade==1:
			return tira(u'%d grupo de %s em %s' %(self.quantidade, self.apettipo, self.metoesta))
		else:
			return tira(u'%d grupos de %s em %s' %(self.quantidade, self.apettipo, self.metoesta))

class ArraTemps(models.Model):#15
	''' os tipos de caracteristicas temporais que serão utilizadas no banco.
	Ex: tempo total de 1 levantamento '''
	arratemp=models.CharField(u'organização do tempo', max_length=100, unique=True)
	descricao=models.TextField(u'descrição')
	class Meta:
		db_table='tbl_arranjos_temporais'
		ordering=['arratemp']
	def __unicode__(self):
		return self.descricao

class UnidTemps(models.Model):#16
	''' define quais undiades temporais serão usadas no banco. Ex: segundo, minuto...'''
	unidtemp=models.CharField(u'unidade do tempo', max_length=100, unique=True)
	descricao=models.TextField(u'descrição', blank=True,  null=True)

	class Meta:
		db_table='tbl_unidades_temporais'

	def __unicode__(self):
		return self.unidtemp

class ArraTempEstas(models.Model):  #17
	''' indica em que unidade aquela caracteristica temporal será mensurada '''
	arratemp=models.ForeignKey(ArraTemps)
	unidtemp=models.ForeignKey(UnidTemps)
	quantidade=models.FloatField(blank=True, null=True)
	outra_descricao=models.TextField(u'outras medidas dos arranjo temporal', blank=True, null=True)
	class Meta:
		db_table='tbl_arranjos_estacoes_temporais'
		unique_together=('arratemp','unidtemp','quantidade','outra_descricao')
		ordering=['arratemp','unidtemp','quantidade']
	def __unicode__(self):
		if self.quantidade is None and self.outra_descricao == '' :
			return tira(u'%s %s'%(self.unidtemp, self.arratemp))
		if self.quantidade is None and self.outra_descricao != '' :
			return tira(u'%s: %s %s'%(self.arratemp, self.outra_descricao, self.unidtemp))
		if self.outra_descricao == '':
			if self.quantidade==1:
				ore=str(self.unidtemp)
				ore=ore.strip(ore[-1:])
				return tira(u'%s: %d %s'%(self.arratemp, self.quantidade, ore))
			else:
				return tira(u'%s: %d %s'%(self.arratemp, self.quantidade, self.unidtemp))

class MontaEstaTemps(models.Model):#18
	''' montar a estaćão quanto aos atributos espaciais. Associa o apetrecho e características a ele atribuída e os arranjos espacias'''
	metoestat=models.ForeignKey(MetoEstas)
	arratempesta=models.ForeignKey(ArraTempEstas, verbose_name=u'arranjo temporal na estação')
	#quantapetesta=models.ForeignKey(QuantApetEstas, verbose_name=u'medida do quantitativo do arranjo')
	class Meta:
		db_table='tbl_monta_estacoes_temporais'
		unique_together=('metoestat','arratempesta')
		ordering=['metoestat__metoempr__empreendimento__empreendimento','metoestat__metoempr__metogrup__metodo__metodo','arratempesta__arratemp']
	def __unicode__(self):
		return tira(u'%s. %s' %(self.metoestat,self.arratempesta))

class MontaEstaEspas(models.Model):#19
	''' montar a estaćão quanto aos atributos espaciais. Associa o apetrecho e características a ele atribuída e os arranjos espacias'''
	metoesta=models.ForeignKey(MetoEstas)
	arraespaesta=models.ForeignKey(ArraEspaEstas, verbose_name=u'arranjo espacial na estação')
	#quantapetesta=models.ForeignKey(QuantApetEstas, verbose_name=u'medida do quantitativo do arranjo')
	ordering=['metoesta__metoempr__empreendimento__empreendimento','metoesta__metoempr__metogrup__metodo__metodo','arraespaesta__arraespa']

	class Meta:
		db_table='tbl_monta_estacoes_espaciais'
		unique_together=('metoesta','arraespaesta')
	def __unicode__(self):
		return tira(u'%s. %s'%(self.metoesta,self.arraespaesta))

class Metodosp(models.Model):#9
	''' relaciona metodo e empreendimento '''
	metodo=models.ForeignKey(Metodos, blank=True, null=True)
	empreendimento=models.ForeignKey(Empreendimentos, blank=True, null=True)
	var_biodiv=models.TextField(blank=True, null=True)
	var_esfor=models.TextField(blank=True, null=True)

	class Meta:
		db_table='tbl_metodosp'
		unique_together=('metodo','empreendimento')
	def __unicode__(self):
		return u'%s de %s'%(self.metodo,self.empreendimento)

class MPP(models.Model):#9
	''' relaciona metodo e empreendimento. Define as variaveis biodiv e esfor. descreve o metodo e indica tipo de local das amostragens'''
	TIPO_LOCAL=(
		(u'parc_terr_defi',u'parcela terrestre definida'),
		(u'parc_aqua_defi',u'parcela aquatica definida'),
		(u'parc_ripa_defi',u'parcela riparia definida'),
		(u'parc_aqua_ripa_def',u'parcela aquatica e riparia definida'),
		(u'tril_terr_def',u'trilha terrestre definida'),
		(u'tril_aqua_def',u'trilha aquatica definida'),
		(u'ua_avul_terr',u'ua avulsa terrestre'),
		(u'ua_avul_aqua',u'ua avulsa aquatica'),
		)

	metodo=models.ForeignKey(MetoEmprs, unique=True)
	var_biodiv=models.TextField(blank=True, null=True)
	var_esfor=models.TextField(blank=True, null=True)
	descricao=models.TextField(blank=True, null=True)
	tipo_local = models.CharField(max_length=25, choices=TIPO_LOCAL, blank=True, null=True, default=None)
	class Meta:
		ordering=['metodo__empreendimento__empreendimento','metodo__metogrup__metodo__metodo']
	def __unicode__(self):
		return u'%s'%self.metodo
  
#AtriEspas,UnidEspas,AtriUnidEspas,ArraEspas,ArraEspaEstas,Apetrechos,
#TipoEsfoEspas,ApetTipos,Metodos,GrupoBioticos,MetoGrups,MetoEmprs,MetoEstas,
#QuantApetEstas,ArraTemps,UnidTemps,ArraTempEstas,MontaEstaTemps, MontaEstaEspas
class Atributos(models.Model):
	tipo_valor = models.CharField(max_length=1, blank=True)
	nome_atributo_cabecalho_coluna = models.CharField(max_length=40, blank=True)
	legenda = models.CharField(max_length=255, blank=True)
	descricao = models.TextField(blank=True)
	referencia = models.CharField(max_length=1, blank=True)
	unidade_utilizada = models.CharField(max_length=55, blank=True)
	class Meta:
		db_table = u'tbl_atributos'
		ordering=('nome_atributo_cabecalho_coluna',)
	def __unicode__(self):
		return self.nome_atributo_cabecalho_coluna
#PARTE2
class Coordenadas(models.Model):
	orientacao = models.CharField(max_length=8, blank=True, null=True)
	datum = models.CharField(max_length=25, default='wgs84', blank=True, null=True)
	ref=models.TextField(blank=True, null=True)
	empreendimento=models.ForeignKey(Empreendimentos,blank=True, null=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	localidade=models.CharField(max_length=15, default='inicio', blank=True, null=True)

	class Meta:
		db_table = u'tbl_coordenadas'
		unique_together=('ref','empreendimento','latitude','longitude','localidade')
	def __unicode__ (self):
		return u'%s->  lat(%s)--long(%s)'%(self.id,self.latitude,self.longitude)

class Inclinacoes(models.Model):
	coordenada=models.ForeignKey(Coordenadas, null=True, blank=True)
	empreendimento=models.ForeignKey(Empreendimentos, null=True, blank=True)
	ref=models.TextField(blank=True, null=True)
	dist_perpend_trilha = models.FloatField(null=True, blank=True)
	inclinacao = models.FloatField()
	dt_observacao = models.DateField(null=True, blank=True)
	coletor_emp=models.ForeignKey(Empresas,null=True, blank=True)
	coletor_pess=models.ForeignKey(Pessoas,null=True, blank=True)

	class Meta:
		db_table = u'tbl_inclinacoes'
	def __unicode__ (self):
		return u'%s->  inclinação --(%s) em (%s)'%(self.id,self.inclinacao,self.empreendimento)



class Topografias(models.Model):
	coordenada=models.ForeignKey(Coordenadas, null=True, blank=True)
	dist_perpend_trilha = models.FloatField(null=True, blank=True)
	alt_mar = models.FloatField()
	empreendimento=models.ForeignKey(Empreendimentos, null=True, blank=True)
	ref=models.TextField(blank=True, null=True)
	coletor_emp=models.ForeignKey(Empresas, null=True, blank=True)
	coletor_pess=models.ForeignKey(Pessoas, null=True, blank=True)
	class Meta:
		db_table = u'tbl_topografias'
	def __unicode__ (self):
		return u'altura no nivel do mar --> %s em %s'% (self.alt_mar,self.empreendimento)

class Solos(models.Model):
	coordenada=models.ForeignKey(Coordenadas, null=True, blank=True)
	empreendimento=models.ForeignKey(Empreendimentos, null=True, blank=True)
	ref=models.TextField(blank=True, null=True)
	dist_perpend_trilha = models.FloatField(null=True, blank=True)
	atributo = models.ForeignKey(Atributos, null=True, blank=True)
	vlr=models.FloatField()
	dt_observacao = models.DateField(null=True, blank=True)
	coletor_emp=models.ForeignKey(Empresas,null=True, blank=True)
	coletor_pess=models.ForeignKey(Pessoas,null=True, blank=True)

	class Meta:
		db_table = u'tbl_solos'
	def __unicode__ (self):
		return u'%s->  solo --(%s) vlr: (%s)'%(self.id,self.atributo,self.vlr)

class GradesModulos(models.Model):
	nome = models.CharField(max_length=50)
	pessoa = models.ForeignKey(Pessoas, null=True, blank=True)
	empreendimento=models.ForeignKey(Empreendimentos)
	tipo = models.CharField(max_length=1, help_text='')
	qnt_trilhas = models.IntegerField(default=2)
	abrev=models.CharField(max_length=75)
	class Meta:
		db_table = u'tbl_grades_modulos'
 		unique_together=('empreendimento','nome')
	def __unicode__(self):
		return self.nome

class Trilhas(models.Model):
	nome = models.CharField(max_length=50)
	grade_modulo = models.ForeignKey(GradesModulos)
	topografia=models.ManyToManyField(Topografias, null=True, blank=True)
	inclinacao=models.ManyToManyField(Inclinacoes, null=True, blank=True)
	coordenada=models.ManyToManyField(Coordenadas, null=True, blank=True)
	comp = models.FloatField()
	rapeld = models.BooleanField(default=True)
	class Meta:
		db_table = u'tbl_trilhas'
		unique_together=('grade_modulo','nome')
	def __unicode__(self):
		return self.nome

class Parcelas(models.Model):
	trilha = models.ForeignKey(Trilhas, null=True, blank=True)
	nome = models.CharField(max_length=80)
	topografia=models.ManyToManyField(Topografias, null=True, blank=True)
	inclinacao=models.ManyToManyField(Inclinacoes, null=True, blank=True)
	coordenada=models.ManyToManyField(Coordenadas, null=True, blank=True)
	dist_paralela_trilha = models.IntegerField(null=True, blank=True)
	dist_perpend_trilha = models.IntegerField(null=True, blank=True)
	segue_curva_nivel = models.BooleanField(default=True)
	comprimento = models.FloatField(null=True, blank=True)
	obs = models.TextField(blank=True)
	class Meta:
		db_table = u'tbl_parcelas'
		unique_together=('trilha','nome')
	def __unicode__(self):
		return self.nome

class UaAvulsas(models.Model):
	nome=models.CharField(max_length=80, null=True, blank=True)
	empreendimento=models.ForeignKey(Empreendimentos, null=True, blank=True)
	descricao = models.TextField(blank=True)
	topografia=models.ManyToManyField(Topografias, null=True, blank=True)
	inclinacao=models.ManyToManyField(Inclinacoes, null=True, blank=True)
	coordenada=models.ManyToManyField(Coordenadas, null=True, blank=True)
	dist = models.FloatField(null=True, blank=True)
	comprimento = models.FloatField(null=True, blank=True)
	segue_curva_nivel = models.BooleanField(default=False)
	class Meta:
		db_table = u'tbl_ua_avulsas'
	def __unicode__(self):
		return self.nome

class Campanhas(models.Model):
	empreendimento = models.ForeignKey(Empreendimentos)
	pessoa = models.ForeignKey(Pessoas,null=True, blank=True)
	descricao = models.CharField(max_length=200, blank=True)
	dt_inicio = models.DateField(null=True, blank=True)
	dt_fim = models.DateField(null=True, blank=True)
	precip_periodo = models.FloatField(null=True, blank=True)
	temp_periodo = models.FloatField(null=True, blank=True)
	metodo = models.ForeignKey(MPP, null=True, blank=True)
	num_campanha = models.IntegerField(null=True, blank=True)
	class Meta:
		db_table = u'tbl_campanhas'
		unique_together=('empreendimento','metodo','num_campanha')
	def __unicode__ (self):
		return u'campanha número:%s'%self.num_campanha
	#	return u'%s->resp:%s; metodo:%s; campanha número:%s )'%(self.empreendimento,self.pessoa,self.metodo,self.num_campanha)


class Levantamentos(models.Model):
	metodo = models.ForeignKey(MPP,null=True, blank=True)
	campanha = models.ForeignKey(Campanhas,null=True, blank=True)
	descricao = models.CharField(max_length=20, blank=True)
	dt_inicial = models.DateField(null=True, blank=True)
	dt_final = models.DateField(null=True, blank=True)
	hr_inicial = models.TimeField(null=True, blank=True)
	hr_final = models.TimeField(null=True, blank=True)
	temp_inicial = models.FloatField(null=True, blank=True)
	temp_final = models.FloatField(null=True, blank=True)
	lat_inicial= models.FloatField(null=True, blank=True)
	lat_final= models.FloatField(null=True, blank=True)
	long_inicial= models.FloatField(null=True, blank=True)
	long_final= models.FloatField(null=True, blank=True)
	datum= models.CharField(max_length=20, null=True, blank=True)
	tipo_ua = models.CharField(max_length=1,null=True, blank=True)
	id_ua = models.IntegerField(null=True, blank=True)
	class Meta:
		db_table = u'tbl_levantamentos'
		unique_together=('metodo','campanha','descricao','dt_inicial','dt_final','hr_inicial','hr_final','temp_inicial','temp_final','lat_inicial','lat_final','long_inicial','long_final','tipo_ua','id_ua')


class DadosColetaAvulsa(models.Model):
	coordenada = models.ForeignKey(Coordenadas,null=True, blank=True)
	empreendimento = models.ForeignKey(Empreendimentos,null=True, blank=True)
	campanha = models.ForeignKey(Campanhas,null=True, blank=True)
	obs=models.TextField(null=True, blank=True)
	class Meta:
		db_table = u'tbl_dados_coleta_avulsa'

class AbioticosDate(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.DateField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_date'

class AbioticosFloat(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.FloatField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_float'

class AbioticosInteger(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.IntegerField(null=True, blank=True)
##	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_integer'

class AbioticosText(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.TextField(blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_text'

class AbioticosTime(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.TimeField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_time'

class AbioticosVarchar(models.Model):
	atributo = models.ForeignKey(Atributos)
	abioticos_dado = models.ForeignKey(Levantamentos)
	valor = models.CharField(max_length=255, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_abioticos_varchar'

class AnimaisDados(models.Model):
	levantamento = models.ForeignKey(Levantamentos)
	filo = models.CharField(max_length=45, blank=True)
	classe = models.CharField(max_length=45, blank=True)
	ordem = models.CharField(max_length=45, blank=True)
	familia = models.CharField(max_length=45, blank=True)
	genero = models.CharField(max_length=45, blank=True)
	imprecisao_determinacao = models.CharField(max_length=45, blank=True)
	epiteto_especifico = models.CharField(max_length=45, blank=True)
	autor_epiteto_especifico = models.CharField(max_length=100, blank=True)
	ano_autor_epiteto_especifico = models.CharField(max_length=20, blank=True)
	coletor = models.CharField(max_length=45, blank=True)
	numero_coleta = models.CharField(max_length=20, blank=True)
	lote_individuo = models.CharField(max_length=20, blank=True)
	coleta_avulsa = models.BooleanField(default=False)
	posicionamento = models.CharField(max_length=1, blank=True)
	superfamilia = models.CharField(max_length=65, blank=True)
	subfamilia = models.CharField(max_length=65, blank=True)
	tribo = models.CharField(max_length=65, blank=True)
	subtribo = models.CharField(max_length=65, blank=True)
	col_avulsa = models.ForeignKey(DadosColetaAvulsa, null=True, blank=True)
	class Meta:
		db_table = u'tbl_animais_dados'
	def __unicode__(self):
		return '%s %s %s' %(self.genero, self.imprecisao_determinacao,self.epiteto_especifico)


class AnimaisDate(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.DateField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_date'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)
class AnimaisFloat(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.FloatField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_float'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)
class AnimaisInteger(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.IntegerField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_integer'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class AnimaisText(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.TextField(blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_text'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class AnimaisTime(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.TimeField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_time'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class AnimaisVarchar(models.Model):
	atributo = models.ForeignKey(Atributos)
	animais_dado = models.ForeignKey(AnimaisDados)
	valor = models.CharField(max_length=255, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_animais_varchar'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasDados(models.Model):
	col_avulsa = models.ForeignKey(DadosColetaAvulsa,null=True, blank=True)
	levantamento = models.ForeignKey(Levantamentos)
	divisao = models.CharField(max_length=45, blank=True)
	classe = models.CharField(max_length=45, blank=True)
	ordem = models.CharField(max_length=45, blank=True)
	familia = models.CharField(max_length=45, blank=True)
	genero = models.CharField(max_length=45, blank=True)
	imprecisao_determinacao = models.CharField(max_length=10, blank=True)
	epiteto_especifico = models.CharField(max_length=45, blank=True)
	autor_epiteto_especifico = models.CharField(max_length=100, blank=True)
	variedade = models.CharField(max_length=255, blank=True)
	autor_variedade = models.CharField(max_length=100, blank=True)
	coletor = models.CharField(max_length=45, blank=True)
	numero_coleta = models.CharField(max_length=20, blank=True)
	coleta_avulsa = models.BooleanField(default=False)
	posicionamento = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_dados'

class PlantasDate(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.DateField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_date'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasFloat(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.FloatField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_float'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasInteger(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.IntegerField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_integer'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasText(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.TextField(blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_text'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasTime(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.TimeField(null=True, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_time'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)

class PlantasVarchar(models.Model):
	atributo = models.ForeignKey(Atributos)
	plantas_dado = models.ForeignKey(PlantasDados)
	valor = models.CharField(max_length=255, blank=True)
#	situacao = models.CharField(max_length=1, blank=True)
	class Meta:
		db_table = u'tbl_plantas_varchar'
	def __unicode__(self):
		return u'%s: %s' %(self.atributo, self.valor)


