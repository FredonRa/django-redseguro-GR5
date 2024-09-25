from django.db import models

# Create your models here.
from django.db import models
from pasos.models import Paso

# Create your models here.
class Opcion(models.Model):
    opcion_id = models.AutoField(primary_key=True)
    paso = models.ForeignKey(Paso, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    nombre = models.CharField(null=False, max_length=50)