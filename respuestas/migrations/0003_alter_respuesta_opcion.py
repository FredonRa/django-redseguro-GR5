# Generated by Django 5.1 on 2024-10-02 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opciones', '0004_alter_opcion_paso'),
        ('respuestas', '0002_alter_respuesta_opcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='opcion',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='opciones.opcion'),
        ),
    ]