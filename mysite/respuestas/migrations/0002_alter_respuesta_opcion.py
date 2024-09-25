# Generated by Django 5.1 on 2024-09-17 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opciones', '0002_alter_opcion_paso'),
        ('respuestas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='opcion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='opciones.opcion'),
        ),
    ]