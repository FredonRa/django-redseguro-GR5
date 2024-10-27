from rest_framework import serializers
from .models import PreguntaFrecuente

class PreguntaFrecuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaFrecuente
        fields = ['preguntaFrecuente_id', 'titulo', 'contenido', 'activo']