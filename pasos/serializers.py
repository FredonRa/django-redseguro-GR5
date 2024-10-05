from rest_framework import serializers
from .models import Paso

class PasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paso
        fields = '__all__'     
        
    def create(self, validated_data):
        return Paso.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.paso_id=validated_data.get('paso_id', instance.paso_id)
        instance.gestion=validated_data.get('gestion', instance.gestion)
        instance.nombre=validated_data.get('nombre', instance.nombre)
        instance.orden=validated_data.get('orden', instance.orden)
        instance.fecha_creacion=validated_data.get('fecha_creacion', instance.fecha_creacion)
        instance.save()
        return instance