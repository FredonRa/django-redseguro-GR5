from django.db import models

# Create your models here.

class Gestion (models.Model):
    gestion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=False, max_length=50)
    tipo_gestion = models.ForeignKey('tipoGestiones.Tipo_Gestion', on_delete=models.CASCADE, default=1, related_name='+')
    
    def __str__(self) -> str:
        return self.nombre
