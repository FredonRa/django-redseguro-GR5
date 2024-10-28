from rest_framework import serializers
from .models import TipoGestion

class TipoGestionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGestion
        fields = ['tipo_gestion_id', 'nombre', 'descripcion']