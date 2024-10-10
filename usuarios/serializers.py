from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'     
        
    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('mail', instance.mail)
        instance.save()
        return instance