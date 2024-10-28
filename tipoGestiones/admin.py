from django.contrib import admin
from .models import Tipo_Gestion

# Register your models here.
class TipoGestionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion'] 
    pass

admin.site.register(Tipo_Gestion, TipoGestionAdmin)