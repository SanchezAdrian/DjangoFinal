from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from nucleo.models import Perfil
from datetime import datetime, date
from django.utils.dateparse import parse_date
class Fecha(forms.DateInput):
    input_type ='date'

class validate(): #
    def validate_dni(self, dni):
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9:
            dig_control = dni[8]
            dni = dni[:8]
            if dni[0] in dig_ext:
                dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) \
                and tabla[int(dni)%23] == dig_control
        return False

    def validateCadena(self, dni):
        if dni[:8].isnumeric():
            if dni[8:9].isalpha():
                return True
        return False



class CreacionUsuarioForm(UserCreationForm):
    email=forms.EmailField(required=True,help_text="Requerido.")
    Dni = forms.CharField(required=True,help_text="Requerido.")
    Nombre = forms.CharField(required=True,help_text="Requerido.")
    Apellidos = forms.CharField(required=True,help_text="Requerido.")
    Direccion = forms.CharField(required=True,help_text="Requerido.")
    Telefono =forms.CharField(required=True,help_text="Requerido.")
    FechaNacimiento = forms.DateField(widget=Fecha())

   
    class Meta:
        model = User
        fields=('username','password1','password2','email','Dni','Nombre','Apellidos','Direccion','Telefono','FechaNacimiento')
        

    def clean_email(self):
        value=self.cleaned_data['email']
        print(self.data['FechaNacimiento'])
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError("Email ya registrado, utilize otro")
        if not validate().validate_dni(self.data['Dni']):
            raise forms.ValidationError("Asegurese de que el DNI es correcto")
        if len(self.data['Dni'])<9:
            raise forms.ValidationError("DNI incompleto")
        if not self.data['Telefono'].isnumeric():
            raise forms.ValidationError("Solo numeros en el campo de telefono por favor")
        if len(self.data['Telefono'])<9:
            raise forms.ValidationError("Telefono incompleto")
        if parse_date(self.data['FechaNacimiento'])>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        
        return value    



    def save(self, commit=True):
        user = super(CreacionUsuarioForm, self).save()
        user.email = self.cleaned_data["email"]
        user.perfil.Dni = self.cleaned_data['Dni']
        user.perfil.Nombre = self.cleaned_data['Nombre']
        user.perfil.Apellidos = self.cleaned_data['Apellidos']
        user.perfil.Direccion = self.cleaned_data['Direccion']
        user.perfil.Telefono = self.cleaned_data['Telefono']
        user.perfil.FechaNacimiento = self.cleaned_data['FechaNacimiento']
        user.save()
        return user

class CreacionPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields=('Dni','Nombre','Apellidos','Direccion','Telefono','FechaNacimiento')
    def clean(self):
        if not validate().validateCadena(self.data['Dni']):
            raise forms.ValidationError("Revise que el dni sea correcto(00000000A")
        if not validate().validate_dni(self.data['Dni']):
            raise forms.ValidationError("Asegurese de que el DNI es correcto")
        if len(self.data['Dni'])<9:
            raise forms.ValidationError("DNI incompleto")
        if not self.data['Telefono'].isnumeric():
            raise forms.ValidationError("Solo numeros en el campo de telefono por favor")
        if len(self.data['Telefono'])<9:
            raise forms.ValidationError("Telefono incompleto")
        if parse_date(self.data['FechaNacimiento'])>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        return self.cleaned_data['FechaNacimiento']

    def save(self, commit=True):
        perfil = super(CreacionPerfilForm, self).save()
        perfil.save()
        return perfil

class PerfilAdmin(forms.ModelForm):
    class Meta:
        model = Perfil
        fields=('Dni','Nombre','Apellidos','Direccion','Telefono','FechaNacimiento','Rol','Activado')
    def clean(self):
        if not validate().validateCadena(self.cleaned_data['Dni']):
            raise forms.ValidationError("Revise que el dni sea correcto(00000000A")
        if not validate().validate_dni(self.cleaned_data['Dni']):
            raise forms.ValidationError("Asegurese de que el DNI es correcto")
        if len(self.cleaned_data['Dni'])<9:
            raise forms.ValidationError("DNI incompleto")
        if not self.cleaned_data['Telefono'].isnumeric():
            raise forms.ValidationError("Solo numeros en el campo de telefono por favor")
        if len(self.cleaned_data['Telefono'])<9:
            raise forms.ValidationError("Telefono incompleto")
        if self.cleaned_data['FechaNacimiento']>date.today():
            raise forms.ValidationError("La fecha no puede ser superior al dia de hoy")
        return self.cleaned_data
        
 

