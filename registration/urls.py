from django.contrib import admin
from django.urls import path
from registration import views

urlpatterns = [
    path('registro', views.RegistroView.as_view(), name="registro"),
    path('profile/<int:pk>',views.profileCliente.as_view(success_url="/"),name="profile"),
]