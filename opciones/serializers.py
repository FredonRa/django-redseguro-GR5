from rest_framework import serializers
from .models import Opcion

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'

    def create(self, validated_data):
        return Opcion.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
    #     instance.save()
    #     return instance