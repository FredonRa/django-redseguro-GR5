from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(null=False, max_length=50)
    apellido = models.CharField(null=False, max_length=50)
    dni = models.CharField(null=False, max_length=20)

class Conversacion(models.Model):
    conversacion_id = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=True)

class Gestion(models.Model):
    gestion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=True, max_length=150)
    fecha_creacion = models.DateTimeField(null=False)
    
class Paso(models.Model):
    paso_id = models.AutoField(primary_key=True)
    gestion_id = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    nombre = models.CharField(null=False, max_length=50)
    orden = models.IntegerField(null=False)
    fecha_creacion = models.DateTimeField(null=False)

class Opcion(models.Model):
    opcion_id = models.AutoField(primary_key=True)
    paso_id = models.ForeignKey(Paso, on_delete=models.CASCADE)
    nombre = models.CharField(null=False, max_length=50)

class Respuesta(models.Model):
    respuesta_id = models.AutoField(primary_key=True)
    opcion_id = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    contenido = models.CharField(null=False, max_length=250)

# Entidad Relacion
class Conversacion_Gestion(models.Model):
    conversacion_gestion_id = models.AutoField(primary_key=True)
    conversacion_id = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    gestion_id = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    
class Conversacion_Paso(models.Model):
    conversacion_paso_id = models.AutoField(primary_key=True)
    conversacion_gestion_id = models.ForeignKey(Conversacion_Gestion, on_delete=models.CASCADE)
    paso_id = models.ForeignKey(Paso, on_delete=models.CASCADE)
    
class Conversacion_Opcion(models.Model):
    conversacion_opcion_id = models.AutoField(primary_key=True)
    conversacion_paso_id = models.ForeignKey(Conversacion_Paso, on_delete=models.CASCADE)
    opcion_id = models.ForeignKey(Opcion, on_delete=models.CASCADE)

class Conversacion_Respuesta(models.Model):
    conversacion_respuesta_id = models.AutoField(primary_key=True)
    conversacion_opcion_id = models.ForeignKey(Conversacion_Opcion, on_delete=models.CASCADE)
    respuesta_id = models.ForeignKey(Respuesta, on_delete=models.CASCADE)


# models.ForeignKey(Reporter, on_delete=models.CASCADE)