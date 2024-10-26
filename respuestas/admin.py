from django.contrib import admin
from .models import Respuesta

# Register your models here.
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['opcion', 'contenido'] 
    pass

admin.site.register(Respuesta, RespuestaAdmin)