from django.contrib import admin
from .models import Gestion

# Register your models here.
class GestionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'tipo_gestion'] 
    pass

admin.site.register(Gestion, GestionAdmin)