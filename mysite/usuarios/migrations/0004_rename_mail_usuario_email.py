# Generated by Django 5.1 on 2024-09-12 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuario_contrasenia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='mail',
            new_name='email',
        ),
    ]