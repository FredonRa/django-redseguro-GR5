# Generated by Django 5.1 on 2024-09-10 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversaciones', '0001_initial'),
        ('usuarios', '0003_usuario_contrasenia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversacion',
            name='fecha_inicio',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='conversacion',
            name='usuario_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuario'),
        ),
    ]
