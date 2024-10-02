from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Conversacion(models.Model):
    conversacion_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)