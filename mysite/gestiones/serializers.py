from rest_framework import serializers
from .models import Gestion


class GestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestion
        fields = '__all__'     
        
    def create(self, validated_data):
        return Gestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id_gestion = validated_data.get('id gestion', instance.id_gestion)
        instance.nombre_gestion= validated_data.get('nombre_gestion', instance.nombre_gestion)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()
        return instance