from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    apellido = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, unique=True)
    contrasenia = models.CharField(null=False, max_length=10, default="12345")

    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    