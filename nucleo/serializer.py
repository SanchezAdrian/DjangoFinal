from rest_framework import serializers
from nucleo.models import Perfil, User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PerfilUserSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    class Meta:
        model = Perfil
        fields = ('id','Dni','Nombre','Apellidos','Direccion','FechaNacimiento','Telefono','Activado','user')
    def create(self, validate_data):
        userInstance = User.objects.get(validate_data)
        instance = Perfil.objects.create(**validate_data,User=userInstance)
        return instance

class PerfilSerializers(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('id','Dni','Nombre','Apellidos','Direccion','FechaNacimiento','Telefono','Rol','Activado')


