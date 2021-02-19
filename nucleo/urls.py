from django.contrib import admin
from django.urls import path
from nucleo.views import *

urlpatterns = [
    path('', ListNoticiasView.as_view(), name="home"),
    ##Clientes
    ## Rutas coches
    path('coches_clientes/', CochesClienteView.as_view(), name="coches_clientes"),
    path('crear_coche/',CrearCochesView.as_view(),name="crear_coche"),
    path('update_coche/<int:pk>',UpdateCochesView.as_view(),name="update_coche"),
    path('delete_coche/<int:pk>',DeleteCochesView.as_view(),name="delete_coche"),
    path('detail_coche/<int:pk>',DetailCocheView.as_view(),name="detail_coche"),
    ## Rutas Reparaciones
    path('crear_reparacion/<int:pk>', CrearReparacionView.as_view(), name="crear_reparacion"),
    path('reparaciones_pendientes_clientes/', ReparacionClientePendienteView.as_view(), name="reparaciones_pendientes_clientes"),
    path('reparaciones_hechas_clientes/', ReparacionClienteDoneView.as_view(), name="reparaciones_hechas_clientes"),
    path('detail_reparacion/<int:pk>',DetailReparacionView.as_view(),name="detail_reparacion"),
    path('reparaciones_coches/<int:pk>',ReparacionesCocheView.as_view(),name="reparaciones_coche"),
    ##Mecanico
    ##Reparaciones
    path('reparaciones_mecanicos/', ReparacionMecanicoView.as_view(), name="reparaciones_mecanicos"),
    path('reparaciones_mecanicos/buscar', ReparacionesClientesMecanicoView.as_view(), name="reparaciones_buscar"),
    path('reparaciones/<int:pk>',ReparacionMecanicoExc.as_view(),name="reparaciones_ex"),
    path('reparaciones/',ReparacionMecanicoInc.as_view(),name="reparaciones_in"),
    path('update_reparacion/<int:pk>',RepararCocheView.as_view(),name="reparar"),
    path('coches_clientes/<int:pk>',CochesClienteParametrosView.as_view(),name="coches_clientes_par"),
    path('reparacionesFil/<int:cli>',ReparacionFiltrada.as_view(),name="reparaciones_fil"),
    
    #Ver clientes
    path('clientes/',ListClientesView.as_view(),name="clientes"),
    #Crear PDF
    path('pdf/<int:pk>',CrearPDF.as_view(),name="pdf"),
    #Noticias
    path('crear_noticia/',CrearNoticiaView.as_view(),name="crear_noticia"),
    path('detail_noticia/<int:pk>',DetailNoticiaView.as_view(),name="detail_noticia"),
    path('update_noticia/<int:pk>',UpdateNoticiaView.as_view(),name="update_noticia"),
    path('delete_noticia/<int:pk>',DeleteNoticiaView.as_view(),name="delete_noticia"),
    #Contacto
    path('crear_contacto/',CreateContactoView.as_view(),name="create_contacto"),
    # API 
    path('api/clientes/',Clientes_API.as_view(),name="clientes_api"),
    path('api/clientes/<int:pk>',Clientes_API_DETAIL.as_view(),name="clientes_api_detail"),
    path('api/token/',TestView.as_view(),name="test_api"),
    path('api/register/',RegisterApi.as_view(),name="register_api"),
    
    path('ups',ups),


] 