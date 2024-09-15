from django.db import models

# Create your models here.
from django.db import models
from opciones.models import Opcion

# Create your models here.
class Respuesta(models.Model):
    respuesta_id = models.AutoField(primary_key=True)
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, blank=True, null=True)
    contenido = models.CharField(null=False, max_length=255)