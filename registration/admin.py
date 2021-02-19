from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from jet.admin import CompactInline
from nucleo.models import *
from django import forms
from registration.forms import validate, PerfilAdmin




class PerfilInLine(CompactInline):
    model = Perfil
    form = PerfilAdmin
    can_delete = False
    verbose_name_plural ='Perfil'
    fk_name = 'user'
    
class CustomUserAdmin(UserAdmin): #
    inlines = (PerfilInLine, )
    list_display = ('username','email','Dni','Rol')
    list_filter = ('username','email')

    def get_fieldsets(self, request, obj=None):
        fields = super().get_fieldsets(request, obj)
        new = []
        for name, fields_dict in fields:
            if fields_dict['fields'] == ('first_name', 'last_name', 'email'):
                fields_dict['fields'] = ('email',)
            new.append((name, fields_dict))
        return new
    
    def Dni(self, obj):
        Dni = obj.perfil.Dni
        return Dni
    Dni.short_description = 'Dni'
    
    
    def Rol(self, obj):
        if obj.perfil.Rol == 1:
            Rol = 'Cliente'
        else:
            Rol = 'Mecanico'
        return Rol
    Rol.short_description = 'Rol'
    
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    @staticmethod
    def autocomplete_search_fields():
        return 'Dni','Nombre','Apellidos','Direccion','Telefono','FechaNacimiento','Rol'

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


