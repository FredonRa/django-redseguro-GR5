from django.db import models

# Create your models here.
class Pasos(models.Model):
    pasos_id = models.AutoField(primary_key=True)
    gestion_id = models.AutoField(primary_key=True)
    nombre_paso = models.CharField(null=False, max_length=50)
    orden = models.AutoField(primary_key=True)
    

    
    