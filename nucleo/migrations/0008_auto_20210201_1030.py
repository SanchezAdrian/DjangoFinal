# Generated by Django 3.1.4 on 2021-02-01 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0007_auto_20210201_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='Rol',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Cliente'), (2, 'Mecanico')], default=1, null=True),
        ),
    ]