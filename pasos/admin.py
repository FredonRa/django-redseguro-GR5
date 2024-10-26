from django.contrib import admin
from .models import Paso

# Register your models here.
class PasoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'gestion', 'orden'] 
    pass

admin.site.register(Paso, PasoAdmin)
