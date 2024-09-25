from django.db import models
from conversaciones.models import Conversacion

# Create your models here.

class Gestion (models.Model):
    gestion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=False, max_length=50)
    

    
    