from django.db import models

# Create your models here.
class Paso(models.Model):
    paso_id = models.AutoField(primary_key=True)
    gestion = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    orden = models.AutoField(primary_key=True)
    

    
    