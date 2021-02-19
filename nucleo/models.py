from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField


# Create your models here.

class Perfil(models.Model):

    CLIENTE = 1
    MECANICO = 2 
    ROLE_CHOICES = (
        (CLIENTE, 'Cliente'),
        (MECANICO, 'Mecanico')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Dni=models.CharField(max_length=9,unique=True,null=True) 
    Nombre=models.CharField(max_length=30,null=True)
    Apellidos=models.CharField(max_length=70,null=True)
    Direccion=models.CharField(max_length=50,null=True)
    Telefono=models.CharField(max_length=9,null=True)
    FechaNacimiento=models.DateField(null=True, verbose_name="Fecha nacimiento")
    Rol=models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=1,null=True, blank=True)
    Activado=models.BooleanField(default="False")

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_perfil(sender, instance, **kwargs):
        instance.perfil.save()

    @staticmethod
    def autocomplete_search_fields():
        return 'Dni','Nombre','Apellidos','Direccion','Telefono','FechaNacimiento','Rol'

    def get_username(self):
        return self.username

    User.add_to_class("__str__", get_username)

    

class Coche(models.Model):
    Matricula=models.CharField(max_length=7)
    Marca=models.CharField(max_length=20)
    Modelo=models.CharField(max_length=30)
    Color=models.CharField(max_length=20)
    FechaMatriculacion=models.DateField(verbose_name="Fecha de matriculacion")
    Imagen=models.ImageField(upload_to='coches', null=True)
    Perfil=models.ForeignKey(Perfil,on_delete=models.CASCADE, verbose_name="Propietario")

    def __str__(self):
        return self.Matricula
    
    @staticmethod
    def autocomplete_search_fields():
        return 'Marca','Modelo','Color','FechaMatriculacion'

    

class Reparacion(models.Model):
    FechaSolicitud=models.DateField( verbose_name="Fecha solicitud")
    FechaArreglo=models.DateField(null=True, verbose_name="Fecha arreglo")
    Motivo=models.CharField(max_length=150)
    Observaciones=models.CharField(max_length=80,null=True)
    Arreglado=models.BooleanField(default=False, verbose_name="Estado")
    Propietario=models.ForeignKey(Perfil,on_delete=models.CASCADE,null=True)
    Coches=models.ForeignKey(Coche,on_delete=models.CASCADE, verbose_name="coche")
    Perfiles=models.ManyToManyField(Perfil,related_name="Mecanicos")

    def __str__(self):
        return self.Motivo
    class Meta:
        verbose_name_plural="Reparaciones"


class Noticia(models.Model):
    Titulo=models.CharField(max_length=50)
    Texto=RichTextField(max_length=300)
    Foto=models.ImageField(upload_to='noticias')
    FechaCreacion=models.DateField( verbose_name="Fecha creacion")
    FechaModificacion=models.DateField(null=True, verbose_name="Fecha modificacion")
    Creador=models.ForeignKey(Perfil,on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo

class Contacto(models.Model):
    Problema=models.CharField(max_length=100)
    Texto=models.CharField(max_length=300)
    FechaPeticion=models.DateField( verbose_name="Fecha peticion")
    EmailUsuario=models.CharField(max_length=100, verbose_name="correo contacto")
    Atendido=models.BooleanField(default=False)

    def __str__(self):
        return self.Problema
