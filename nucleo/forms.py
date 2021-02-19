from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from nucleo.models import *
from ckeditor.widgets import CKEditorWidget
from datetime import datetime, date
from django.utils.dateparse import parse_date
from nucleo.apps import Validate

class Fecha(forms.DateInput):
    input_type ='date'

class CreacionCocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields=('Matricula','Marca','Modelo','Color','FechaMatriculacion','Imagen')
        widgets = {
            'FechaMatriculacion': Fecha()
        }
    def clean(self):
        value = self.cleaned_data
        if len(self.cleaned_data['Matricula'])<7:
            raise forms.ValidationError("Matricula incompleta")
        if not Validate.validateMatricula(self.cleaned_data['Matricula']):
            raise forms.ValidationError("formato de matricula incorrecto, debe seguir formato XXXX000")
        if Coche.objects.filter(Matricula=self.cleaned_data['Matricula']).exists():
            raise forms.ValidationError("Esta matricula ya esta en uso, revisela!")
        if self.cleaned_data['FechaMatriculacion']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        return value

class UpdateCocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields=('Matricula','Marca','Modelo','Color','FechaMatriculacion','Imagen')
        widgets = {
            'FechaMatriculacion': Fecha()
        }
    def clean(self):
        value = self.cleaned_data
        if len(self.cleaned_data['Matricula'])<7:
            raise forms.ValidationError("Matricula incompleta")
        if not Validate.validateMatricula(self.cleaned_data['Matricula']):
            raise forms.ValidationError("formato de matricula incorrecto, debe seguir formato XXXX000")
        if self.cleaned_data['FechaMatriculacion']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        return value

class CreacionReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields=('FechaSolicitud','Motivo','Coches','Propietario')

class UpdateReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields=('Observaciones','FechaArreglo','Arreglado')
        widgets = {
            'FechaArreglo': Fecha()
        }

class CreateNoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ('Titulo','Texto','Foto','FechaCreacion','Creador')
        widgets= {
            'FechaCreacion': Fecha(),
            'Texto': CKEditorWidget()
        }

class UpdateNoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields=('Titulo','Texto','Foto','FechaModificacion')
        widgets = {
            'FechaModificacion': Fecha(),
            'Texto': CKEditorWidget()
        }

class CreateContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields=('Problema','Texto','FechaPeticion','EmailUsuario')



 

# Admin 
class CocheAdminForm(forms.ModelForm):

    def clean(self):
        value = self.cleaned_data
        if len(self.cleaned_data['Matricula'])<7:
            raise forms.ValidationError("Matricula incompleta")
        
        if not Validate.validateMatricula(self.cleaned_data['Matricula']):
            raise forms.ValidationError("formato de matricula incorrecto, debe seguir formato XXXX000")
        if Coche.objects.filter(Matricula=self.cleaned_data['Matricula']).exists():
            raise forms.ValidationError("Esta matricula ya esta en uso, revisela!")
        if self.cleaned_data['FechaMatriculacion']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        
        return value   

class ReparacionAdminForm(forms.ModelForm):

    def clean(self):
        value = self.cleaned_data
        if self.cleaned_data['FechaArreglo']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")

class NoticiaAdminForm(forms.ModelForm):
    def clean(self):
        value = self.cleaned_data
        if self.cleaned_data['FechaModificacion']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")

 