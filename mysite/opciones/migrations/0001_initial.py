# Generated by Django 5.1 on 2024-09-15 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pasos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('opcion_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('paso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pasos.paso')),
            ],
        ),
    ]
