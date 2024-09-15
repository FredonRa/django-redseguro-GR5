# Generated by Django 5.1 on 2024-09-15 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestiones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paso',
            fields=[
                ('paso_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('orden', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('gestion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestiones.gestion')),
            ],
        ),
    ]
