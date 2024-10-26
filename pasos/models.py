from django.db import models
from gestiones.models import Gestion

# Create your models here.
class Paso(models.Model):
    paso_id = models.AutoField(primary_key=True)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE, blank=True, null=False, related_name='+', default=1)
    nombre = models.CharField(null=False, max_length=50)
    orden = models.IntegerField(null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre