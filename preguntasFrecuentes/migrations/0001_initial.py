# Generated by Django 5.1 on 2024-10-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaFrecuente',
            fields=[
                ('preguntaFrecuente_id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50)),
                ('contenido', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
    ]