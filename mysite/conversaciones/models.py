from django.db import models
from usuarios.models import Usuario
from django.http import JsonResponse

# Create your models here.
class Conversacion(models.Model):
    conversacion_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=False, default=1)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)
    
def get_field_types(model):
    fields = model._meta.get_fields()
    field_types = {}
    for field in fields:
        field_types[field.name] = type(field).__name__
    return field_types

def field_types_view(request):
    field_types = get_field_types(Conversacion)
    return JsonResponse(field_types)