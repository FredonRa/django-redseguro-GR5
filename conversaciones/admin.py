from django.contrib import admin
from .models import Conversacion

# Register your models here.
class ConversacionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Conversacion, ConversacionAdmin)