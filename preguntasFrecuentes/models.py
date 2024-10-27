from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class PreguntaFrecuente(models.Model):
    preguntaFrecuente_id = models.AutoField(primary_key=True)
    titulo = models.CharField(null=False, max_length=50)
    contenido = models.CharField(null=False, max_length=255)
    activo = models.BooleanField(null=False, default=True)