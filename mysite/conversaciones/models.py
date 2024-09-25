from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Conversacion(models.Model):
    conversacion_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=False, default=1)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)

class Conversacion_Gestion(models.Model):
    conversacion_gestion_id = models.AutoField(primary_key=True)
    conversacion = models.ForeignKey('Conversacion', on_delete=models.CASCADE, related_name='+')
    gestion = models.ForeignKey('gestiones.Gestion', on_delete=models.CASCADE, related_name='+')
    
class Conversacion_Paso(models.Model):
    conversacion_paso_id = models.AutoField(primary_key=True)
    conversacion_gestion = models.ForeignKey('Conversacion_Gestion', on_delete=models.CASCADE, related_name='+')
    paso = models.ForeignKey('pasos.Paso', on_delete=models.CASCADE, related_name='+')
    
class Conversacion_Opcion(models.Model):
    conversacion_opcion_id = models.AutoField(primary_key=True)
    conversacion_paso = models.ForeignKey('Conversacion_Paso', on_delete=models.CASCADE, related_name='+')
    opcion = models.ForeignKey('opciones.Opcion', on_delete=models.CASCADE, related_name='+')

class Conversacion_Respuesta(models.Model):
    conversacion_respuesta_id = models.AutoField(primary_key=True)
    conversacion_opcion = models.ForeignKey('Conversacion_Opcion', on_delete=models.CASCADE, related_name='+')
    respuesta = models.ForeignKey('respuestas.Respuesta', on_delete=models.CASCADE, related_name='+')