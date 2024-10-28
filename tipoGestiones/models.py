from django.db import models

# Create your models here.
class Tipo_Gestion(models.Model):
    tipo_gestion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=False, max_length=50)
    
    def __str__(self) -> str:
        return self.nombre