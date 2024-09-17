from django.db import models
from conversaciones.models import Conversacion

# Create your models here.

class Gestion (models.Model):
    gestion_id = models.AutoField(primary_key=True)
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, blank=True, null=False, default=1)
    nombre = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=False, max_length=50)
    

    
    