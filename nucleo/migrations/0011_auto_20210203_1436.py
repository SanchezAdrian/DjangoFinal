# Generated by Django 3.1.4 on 2021-02-03 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0010_auto_20210203_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparacion',
            name='Perfiles',
            field=models.ManyToManyField(null=True, related_name='Mecanicos', to='nucleo.Perfil'),
        ),
        migrations.AlterField(
            model_name='reparacion',
            name='Reparador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.perfil'),
        ),
    ]