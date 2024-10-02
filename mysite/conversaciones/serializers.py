from rest_framework import serializers
from .models import Conversacion

class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = '__all__'

    def create(self, validated_data):
        return Conversacion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
        instance.save()
        return instance