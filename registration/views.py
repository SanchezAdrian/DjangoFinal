from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django import forms
from registration.forms import  CreacionUsuarioForm, CreacionPerfilForm
from nucleo.models import *





class profileCliente(UpdateView): 
    model = Perfil
    form_class = CreacionPerfilForm
    template_name = 'registration/profile.html'
    success_url = '/'

    def get_succes_url(self):
        return reverse_lazy('profile')+'?login'

    def get_form(self, form_class=None):
        form=super(profileCliente,self).get_form()

        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar datos clientes"
        context['entity'] = 'Perfil'
        context['action'] = 'edit'
        return context
    

    
class RegistroView(CreateView):
   
    form_class=CreacionUsuarioForm
    success_url = '/'
    template_name="registro.html"


    def get_succes_url(self):
        return reverse_lazy('login')+'?register'
    
    def get_form(self, form_class=None): 
        form=super(RegistroView,self).get_form()
        form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Nombre de usuario'})
        form.fields['email'].widget=forms.EmailInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'direccion email'})                                            
        form.fields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Contraseña'})        
        form.fields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Repita contraseña'})    
        form.fields['Dni'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Dni'})    
        form.fields['Nombre'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Nombre'})    
        form.fields['Apellidos'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Ambos apelldios'})    
        form.fields['Direccion'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Direccion de vivienda'})    
        form.fields['Telefono'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Numero de contacto'})    
                                              
                                                   
       
        return form           
 
