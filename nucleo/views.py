from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from nucleo.models import *
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django import forms
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import DetailView
from nucleo.forms import CreacionCocheForm, CreacionReparacionForm, UpdateReparacionForm, CreateNoticiaForm, UpdateNoticiaForm, CreateContactoForm, UpdateCocheForm
from datetime import datetime
from dateutil.relativedelta import relativedelta # uso de relativedata para obtener la edad facilmente
from django_xhtml2pdf.views import PdfMixin 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from nucleo.serializer import PerfilSerializers, UserSerializers, PerfilUserSerializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
# Create your views here.

user_cliente = user_passes_test(lambda user: user.perfil.Rol == 1, login_url='/ups')
user_mecanico = user_passes_test(lambda user: user.perfil.Rol == 2, login_url='/ups')

def es_cliente(view_func):
    decorated_view_func = login_required(user_cliente(view_func))
    return decorated_view_func

def es_mecanico(view_func):
    decorated_view_func = login_required(user_mecanico(view_func))
    return decorated_view_func


@method_decorator(login_required, name='dispatch')
def index(request):
    return render(request, 'index.html')

def ups(request):
    return render(request, 'credenciales.html')

## COCHES CLIENTE

@method_decorator(es_cliente, name='dispatch')
class CrearCochesView(CreateView):
    model = Coche
    form_class=CreacionCocheForm
    template_name="cliente/create_coche.html"
    success_url="/coches_clientes"

   

    def get_succes_url(self):
        return reverse_lazy('coches_clientes')+'?'

    def getPerf(self):
        CrearCochesView.asignarPerfil(self.request.user.perfil)
    
    def get_form(self, form_class=None): 
        form=super(CrearCochesView,self).get_form()
        form.instance.Perfil = self.request.user.perfil
        form.fields['Matricula'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Matricula'})
        form.fields['Marca'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Marca'})
        form.fields['Modelo'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Modelo'})
        form.fields['Color'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Color'})     
                                                                                                                            
        return form           
@method_decorator(es_cliente, name='dispatch')
class UpdateCochesView(UpdateView):
    model = Coche 
    form_class=UpdateCocheForm
    template_name="cliente/create_coche.html"
    success_url="/coches_clientes"

    def get_initial(self):
        initial = super().get_initial()
        initial['FechaMatriculacion'] = Coche.objects.get(id=self.kwargs.get('pk')).FechaMatriculacion
        
    def get_form(self, form_class=None): 
        form=super(UpdateCochesView,self).get_form()
        form.instance.Perfil = self.request.user.perfil
        form.fields['Matricula'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Matricula'})
        form.fields['Marca'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Marca'})
        form.fields['Modelo'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Modelo'})
        form.fields['Color'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Color'})  
        form.fields['FechaMatriculacion'].widget=forms.DateInput()        
                                                                                                                            
        return form           

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Coche'
        context['action'] = 'edit'
        return context
    


@method_decorator(login_required, name='dispatch')
class CochesClienteView(ListView):
    model = Coche 
    template_name = 'cliente/view_coches.html'

    def get_queryset(self):
        return Coche.objects.filter(Perfil=self.request.user.perfil)
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(es_cliente, name='dispatch')  
class DeleteCochesView(DeleteView):
    model = Coche 
    success_url="/coches_clientes"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        #Sobre escribe el metodo get para borrar sin pasar por otra vista y hacerlo atraves del popup
         
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Coche'
        return context
@method_decorator(login_required, name='dispatch')
class DetailCocheView(DetailView):
    model = Coche
    template_name = 'cliente/detail_coche.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

## FIN COCHES CLIENTES

## Reparaciones
@method_decorator(es_cliente, name='dispatch')
class CrearReparacionView(CreateView):
    model = Reparacion
    form_class=CreacionReparacionForm
    template_name="cliente/create_reparacion.html"
    success_url="/coches_clientes"
    now = datetime.now()

    def get_initial(self):
        initial = super().get_initial()
        initial['Coches'] = Coche.objects.get(id=self.kwargs.get('pk'))
        initial['FechaSolicitud'] = self.now.date()
        initial['Propietario'] = self.request.user.perfil

        return initial
    
    def get_succes_url(self):
        return reverse_lazy('coches_clientes')+'?'
    

    def getCoche(self):
        CrearReparacionView.asignarCoche(self.kwargs.get('pk'))
        
    def get_form(self, form_class=None): 
        form=super(CrearReparacionView,self).get_form()
        form.fields['Motivo'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Motivo'})
        form.fields['FechaSolicitud'].widget=forms.HiddenInput()
        form.fields['Coches'].widget=forms.HiddenInput()
        form.fields['Propietario'].widget=forms.HiddenInput()

                                                                                                                                                   
        return form     

   
@method_decorator(es_cliente, name='dispatch')    
class ReparacionClientePendienteView(ListView):
    model = Reparacion 
    template_name = 'cliente/view_reparaciones_pen.html'

    def get_queryset(self):
        return Reparacion.objects.filter(Propietario=self.request.user.perfil).filter(Arreglado=False)
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
@method_decorator(es_cliente, name='dispatch')    
class ReparacionClienteDoneView(ListView):
    model = Reparacion 
    template_name = 'cliente/view_reparaciones_hechas.html'

    def get_queryset(self):
        return Reparacion.objects.filter(Propietario=self.request.user.perfil).filter(Arreglado=True)
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
  ## Mecanicos       

@method_decorator(es_mecanico, name='dispatch')
class ReparacionMecanicoView(ListView):
    model = Reparacion 
    template_name = 'mecanico/view_reparaciones.html'

    def get_queryset(self):
        return Reparacion.objects.exclude(Perfiles__in=[self.request.user.perfil]).filter(Arreglado=False)
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(es_mecanico, name='dispatch')
class ReparacionesClientesMecanicoView(ListView):
    model = Perfil 
    template_name = 'mecanico/buscar_reparacion.html'

    def get_queryset(self):
        
        return Perfil.objects.filter(Rol=1)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        coches = Coche.objects.all()
        context['Coches_list']= coches
        return context

@method_decorator(es_mecanico, name='dispatch')
class ReparacionMecanicoExc(ListView): ##CAMBAIR FILTRO PARA QUE SEA DE LOS QUE NO TIENES Y QUEDE TO GUAY
    model = Reparacion 
    template_name = 'mecanico/asignar.html'


    def get_queryset(self):
        return Reparacion.objects.exclude(Perfiles__in=[self.request.user.perfil]).filter(Arreglado=False)
        #filtramos los coches por el perfil activo
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if(self.kwargs['pk'] is not None):
            reparacion = Reparacion.objects.get(id = self.kwargs['pk'])
            reparacion.Perfiles.add(self.request.user.perfil)
            reparacion.save()
        return context

@method_decorator(es_mecanico, name='dispatch')
class ReparacionFiltrada(ListView):
    model = Reparacion 
    template_name = 'mecanico/reparaciones_filtradas.html'
    success_url = '/reparaciones'
  
    def get_queryset(self):
        c1 = self.request.GET.get('cars')
        
        print('datos')
        print(c1)
        return Reparacion.objects.exclude(Perfiles__in=[self.request.user.perfil]).filter(Arreglado=False).filter(Propietario=Perfil.objects.get(id=self.kwargs['cli'])).filter(Coches=Coche.objects.get(id=c1))
        #filtramos los coches por el perfil activo
    
       
@method_decorator(es_mecanico, name='dispatch')
class ReparacionMecanicoInc(ListView): ##
    model = Reparacion 
    template_name = 'mecanico/asignado.html'


    def get_queryset(self):
        
        return Reparacion.objects.filter(Perfiles__in=[self.request.user.perfil]).filter(Arreglado=False)
        #filtramos los coches por el perfil activo
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(es_mecanico, name='dispatch')
class RepararCocheView(UpdateView):
    model = Reparacion 
    form_class=UpdateReparacionForm
    template_name="mecanico/update_reparacion.html"
    success_url="/reparaciones"
    now = datetime.now()

    def get_initial(self):
        initial = super().get_initial()
        initial['FechaArreglo'] = self.now.date()
        initial['Arreglado'] = True

        return initial

    def get_form(self, form_class=None): 
        form=super(RepararCocheView,self).get_form()
        form.fields['Observaciones'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Motivo'})     
        form.fields['FechaArreglo'].widget=forms.HiddenInput()
        form.fields['Arreglado'].widget=forms.HiddenInput()                                                                                                                                                              
        return form           

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Reparacion'
        context['action'] = 'edit'
        return context

@method_decorator(es_mecanico, name='dispatch')     
class ListClientesView(ListView):
    model = Perfil 
    template_name = 'mecanico/clientes.html'


    def get_queryset(self):
        
        return Perfil.objects.filter(Rol=1)
        #filtramos los coches por el perfil activo
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(es_mecanico, name='dispatch')
class CochesClienteParametrosView(ListView):
    model = Coche 
    template_name = 'cliente/view_coches.html'

    def get_queryset(self):
        return Coche.objects.filter(Perfil=Perfil.objects.get(id=self.kwargs['pk']))
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class ReparacionesCocheView(ListView):
    model = Reparacion 
    template_name = 'mecanico/reparaciones_coche.html'

    def get_queryset(self):
        return Reparacion.objects.filter(Coches=Coche.objects.get(id=self.kwargs['pk'])) 
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['coche']=Coche.objects.get(id=self.kwargs['pk'])
        return context

@method_decorator(login_required, name='dispatch')
class DetailReparacionView(DetailView):
    model = Reparacion
    template_name = 'cliente/detail_reparacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coche']=Reparacion.objects.get(id=self.kwargs['pk']).Coches 
        context['edad']=relativedelta(datetime.now(),Reparacion.objects.get(id=self.kwargs['pk']).Propietario.FechaNacimiento) #Le paso la edad para darle mejor visibilidad
        context['hoy']=datetime.now()
        return context

@method_decorator(login_required, name='dispatch')
class CrearPDF(PdfMixin, DetailView):
    model = Reparacion
    template_name = 'mecanico/pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coche']=Reparacion.objects.get(id=self.kwargs['pk']).Coches 
        context['edad']=relativedelta(datetime.now(),Reparacion.objects.get(id=self.kwargs['pk']).Propietario.FechaNacimiento) #Le paso la edad para darle mejor visibilidad
        context['hoy']=datetime.now()
        return context

#Noticias 
@method_decorator(es_mecanico, name='dispatch')
class CrearNoticiaView(CreateView):
    model = Noticia
    form_class=CreateNoticiaForm
    template_name="mecanico/create_noticia.html"
    success_url="/"
    now = datetime.now()

    def get_initial(self):
        initial = super().get_initial()
        initial['FechaCreacion'] = self.now.date()
        initial['Creador'] = self.request.user.perfil

        return initial
    
    def get_succes_url(self):
        return reverse_lazy('')+'?'
        
    def get_form(self, form_class=None): 
        form=super(CrearNoticiaView,self).get_form()
        form.fields['Titulo'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Titulo'})                                                                                   
        form.fields['FechaCreacion'].widget=forms.HiddenInput()
        form.fields['Creador'].widget=forms.HiddenInput()                                                                                                                                     
        return form     
    
@method_decorator(login_required, name='dispatch')
class ListNoticiasView(ListView):
    model = Noticia 
    template_name = 'index.html'

    def get_queryset(self):
        return Noticia.objects.order_by('-FechaCreacion')
        #filtramos los coches por el perfil activo

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class DetailNoticiaView(TemplateView): #Uso de templateView
    model = Noticia
    template_name = 'mecanico/detail_noticia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticia']=Noticia.objects.get(id=self.kwargs['pk'])
        return context

@method_decorator(es_mecanico, name='dispatch')
class UpdateNoticiaView(UpdateView):
    model = Noticia
    form_class=UpdateNoticiaForm
    template_name="mecanico/update_noticia.html"
    success_url="/"
    now = datetime.now() 

    def get_initial(self):
        initial = super().get_initial()
        initial['FechaModificacion'] = self.now.date()
        return initial
    
    def get_succes_url(self):
        return reverse_lazy('')+'?'
        
    def get_form(self, form_class=None): 
        form=super(UpdateNoticiaView,self).get_form()
        form.fields['Titulo'].widget=forms.TextInput(attrs={'class':'form-control',
                                                    'placeholder':'Titulo'})                                                                                   
        form.fields['FechaModificacion'].widget=forms.HiddenInput()                                                                                                                                 
        return form             

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Noticia'
        context['action'] = 'edit'
        return context

@method_decorator(es_mecanico, name='dispatch')
class DeleteNoticiaView(DeleteView):
    model = Noticia 
    success_url="/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        #Sobre escribe el metodo get para borrar sin pasar por otra vista y hacerlo atraves del popup
         
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Noticia'
        return context

# Contacto

@method_decorator(es_cliente, name='dispatch')
class CreateContactoView(CreateView):
    model = Contacto
    form_class=CreateContactoForm
    template_name="cliente/create_contacto.html"
    success_url="/"
    now = datetime.now()

    def get_initial(self):
        initial = super().get_initial()
        initial['FechaPeticion'] = self.now.date()
        initial['EmailUsuario'] = self.request.user.email

        return initial
    
    def get_succes_url(self):
        return reverse_lazy('')+'?'
        
    def get_form(self, form_class=None): 
        form=super(CreateContactoView,self).get_form()
        form.fields['Problema'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Problema'})
        form.fields['Texto'].widget=forms.Textarea(attrs={'class':'form-control mb2',
                                                    'placeholder':'Texto'})                                                                                     
        form.fields['FechaPeticion'].widget=forms.HiddenInput()
        form.fields['EmailUsuario'].widget=forms.HiddenInput()                                                                                                                                     
        return form   

# API
class Clientes_API(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        clientes = Perfil.objects.filter(Rol=1)
        serializer = PerfilUserSerializers(clientes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PerfilSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BSD_REQUEST)

class Clientes_API_DETAIL(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Perfil.objects.get(id=pk)
        except Perfil.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cliente = Perfil.objects.get(id=pk)
        serializer = PerfilUserSerializers(cliente)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        cli = self.get_object(pk)
        serializer = PerfilSerializers(cli, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cli= self.get_object(pk)
        cli.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestView(APIView):

    def get(self, request, format=None):
        return Response({'detail':"GET Response"})

    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.get(username=data["user"])
        if not user:
            return Response(
                'No default user, please create one',
                status=status.HTTP_404_NOT_FOUND
            )
        
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token[0].key})

class RegisterApi(APIView):
    def get(self, request, format=None):
        return Response({'detail':"GET Response"})
    
    def post(self, request, format=None):
        
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)