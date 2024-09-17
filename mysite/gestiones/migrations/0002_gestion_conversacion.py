# Generated by Django 5.1 on 2024-09-17 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversaciones', '0008_alter_conversacion_usuario'),
        ('gestiones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gestion',
            name='conversacion',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='conversaciones.conversacion'),
        ),
    ]
