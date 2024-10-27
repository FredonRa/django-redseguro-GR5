from django.contrib import admin
from .models import PreguntaFrecuente

# Register your models here.
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'contenido'] 
    pass

admin.site.register(PreguntaFrecuente, PreguntaFrecuenteAdmin)