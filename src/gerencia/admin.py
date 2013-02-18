#-*- coding: utf-8 -*-
from django.contrib import admin
from dados.models import *
from gerencia.models import *
#from usuarios.models import Usuarios
class MontaEstaTempsAdmin(admin.ModelAdmin):
	list_display=('metoestat','arratempesta')
	list_filter=('metoestat__metoempr__empreendimento','arratempesta__arratemp',
'metoestat__metoempr__metogrup__metodo')
#	def listafor(self,obj):
#		return '%s'%(obj.metoestat.metoempr.empreendimento)
class MontaEstaEspasAdmin(admin.ModelAdmin):
	list_display=('metoesta','arraespaesta')
	list_filter=('metoesta__metoempr__empreendimento','arraespaesta__arraespa','metoesta__metoempr__metogrup__metodo')
class MPPAdmin(admin.ModelAdmin):
	list_display=('metodo',)
	list_filter=('metodo__empreendimento__empreendimento','metodo__metogrup__metodo__metodo')
class QuantApetEstasAdmin(admin.ModelAdmin):
	list_display=('quantidade','apettipo','metoesta')
	list_filter=('metoesta__metoempr__empreendimento__empreendimento',
'apettipo','metoesta__metoempr__metogrup__metodo', 'metoesta')
class ApetDefisAdmin(admin.ModelAdmin):
	list_filter=('apetrecho','atriunidespa')
class ApetTiposAdmin(admin.ModelAdmin):
	list_filter=('apetrecho',)
class MetoEmprsAdmin(admin.ModelAdmin):
	list_display=('empreendimento','metogrup')
	list_filter=('empreendimento','metogrup')
class MetoEstasAdmin(admin.ModelAdmin):
	list_display=('metoempr','nome_estac')
	list_filter=('metoempr__empreendimento','metoempr__metogrup','nome_estac')
class AtributosAdmin(admin.ModelAdmin):
	list_display=('nome_atributo_cabecalho_coluna','descricao')
	list_filter=('referencia','legenda','tipo_valor')

admin.site.register(MetoEstas, MetoEstasAdmin)
admin.site.register(QuantApetEstas, QuantApetEstasAdmin)
admin.site.register(MPP, MPPAdmin)
admin.site.register(MontaEstaEspas, MontaEstaEspasAdmin)
admin.site.register(MontaEstaTemps, MontaEstaTempsAdmin)
admin.site.register(ApetDefis, ApetDefisAdmin)
admin.site.register(MetoEmprs, MetoEmprsAdmin)
admin.site.register(ApetTipos, ApetTiposAdmin)
admin.site.register(Atributos, AtributosAdmin)

admin.site.register([AbioticosDate, AbioticosFloat, AbioticosInteger, AbioticosText, AbioticosTime, AbioticosVarchar, AnimaisDados, AnimaisDate, AnimaisFloat, AnimaisInteger, AnimaisText, AnimaisTime, AnimaisVarchar, Apetrechos, ArraEspaEstas, ArraEspas, ArraTempEstas, ArraTemps, AtriEspas, AtriUnidEspas, Campanhas, Coordenadas, DadosColetaAvulsa, Empreendimentos, Empresas, GradesModulos, GrupoBioticos, Inclinacoes,Solos, Levantamentos, MetoGrups, Metodos, Parcelas, Pessoas, PlantasDados, PlantasDate, PlantasFloat, PlantasInteger, PlantasText, PlantasTime, PlantasVarchar, QuantTipoApets, TipoEsfoEspas, Topografias, Trilhas, UaAvulsas, UnidEspas, UnidTemps,CabecalhosLocais,Document,DocumentZip])
