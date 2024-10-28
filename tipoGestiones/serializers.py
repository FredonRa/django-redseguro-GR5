from rest_framework import serializers
from .models import Tipo_Gestion

class TipoGestionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Gestion
        fields = ['tipo_gestion_id', 'nombre', 'descripcion']