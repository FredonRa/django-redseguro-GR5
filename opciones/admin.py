from django.contrib import admin
from .models import Opcion

# Register your models here.
class OpcionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'paso', 'siguiente_paso'] 
    pass

admin.site.register(Opcion, OpcionAdmin)