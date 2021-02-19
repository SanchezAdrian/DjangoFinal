from django.contrib import admin
from nucleo.models import *
from jet.filters import RelatedFieldAjaxListFilter
from jet.admin import CompactInline
from nucleo.forms import CocheAdminForm, ReparacionAdminForm, NoticiaAdminForm


 

class PersonAdmin(admin.ModelAdmin):
    list_filter = (
        ('Perfil', RelatedFieldAjaxListFilter),
    )

class ContactoInLine(admin.ModelAdmin):
    model = Contacto
    list_display = ('EmailUsuario','Atendido','Problema')
    list_filter = ('Atendido', 'EmailUsuario')
    readonly_fields = ('EmailUsuario','Problema','Texto','FechaPeticion')


class CochelInLine(admin.ModelAdmin):
    model = Coche
    form = CocheAdminForm
    list_filter = ('Matricula','FechaMatriculacion')
    list_display = ('Matricula','FechaMatriculacion')

   
    


class ReparacionlInLine(admin.ModelAdmin):
    model = Reparacion    
    form = ReparacionAdminForm
    verbose_name ='Reparaciones'
    list_filter = ('Arreglado', 'FechaSolicitud','FechaArreglo')
    list_display = ('Arreglado','FechaSolicitud','FechaArreglo','Coches')
    readonly_fields = ('Coches','Propietario')

class NoticialInLine(admin.ModelAdmin):
    model = Noticia    
    form = NoticiaAdminForm
    verbose_name_plural ='Noticias'
    list_display = ('FechaCreacion','Creador')
    list_filter = ('FechaCreacion',)
    readonly_fields = ('FechaCreacion','Creador')

  
        

admin.site.register(Contacto, ContactoInLine)
admin.site.register(Noticia, NoticialInLine)
admin.site.register(Reparacion, ReparacionlInLine)
admin.site.register(Coche,CochelInLine)