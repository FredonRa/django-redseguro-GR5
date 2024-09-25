from django.db import models
from gestiones.models import Gestion

# Create your models here.
class Paso(models.Model):
    paso_id = models.AutoField(primary_key=True)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    nombre = models.CharField(null=False, max_length=50)
    orden = models.IntegerField(null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
