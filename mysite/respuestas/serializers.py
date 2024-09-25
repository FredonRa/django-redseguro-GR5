from rest_framework import serializers
from .models import Respuesta

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['respuesta_id', 'opcion', 'contenido']

    def create(self, validated_data):
        return Respuesta.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
    #     instance.save()
    #     return instance