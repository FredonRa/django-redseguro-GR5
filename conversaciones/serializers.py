from rest_framework import serializers
from .models import (Conversacion, Conversacion_Tipo_Gestion, Conversacion_Gestion, 
                     Conversacion_Opcion, Conversacion_Paso, Conversacion_Respuesta)
from respuestas.models import Respuesta
from respuestas.serializers import RespuestaSerializer

class ConversacionSerializer(serializers.ModelSerializer):
    gestion = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion
        fields = '__all__'
        read_only_fields = ['fecha_fin']

    def create(self, validated_data):
        return Conversacion.objects.create(**validated_data)

    def get_gestion(self, obj):
        # Obtener solo la primera gestión, ya que solo puede haber una gestión por conversación
        gestion = Conversacion_Gestion.objects.filter(conversacion=obj).first()
        if gestion:
            return ConversacionGestionSerializer(gestion).data
        return None

    # def get_tipo_gestion(self, obj):
    #     # Obtener solo la primera gestión, ya que solo puede haber una gestión por conversación
    #     tipo_gestion = Conversacion_Tipo_Gestion.objects.filter(conversacion=obj.conversacion_id).first()
    #     if tipo_gestion:
    #         return ConversacionTipoGestionSerializer(tipo_gestion).data
    #     return None
    
class ConversacionTipoGestionSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='tipo_gestion.nombre', read_only=True)
    gestion = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion_Tipo_Gestion
        fields = ['conversacion_tipo_gestion_id', 'nombre', 'conversacion', 'tipo_gestion_id', 'gestion']
        
    def get_gestion(self, obj):
        try:
            gestion = Conversacion_Gestion.objects.get(conversacion_id=obj.conversacion_id)
            return ConversacionGestionSerializer(gestion).data
        except Conversacion_Gestion.DoesNotExist:
            return None

class ConversacionGestionSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='gestion.nombre', read_only=True)
    pasos = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion_Gestion
        fields = ['conversacion_gestion_id', 'nombre', 'pasos']

    def get_pasos(self, obj):
        pasos = Conversacion_Paso.objects.filter(conversacion_gestion=obj)
        return ConversacionPasoSerializer(pasos, many=True).data

class ConversacionPasoSerializer(serializers.ModelSerializer):
    opcion = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion_Paso
        fields = ['conversacion_paso_id', 'paso', 'opcion']

    def get_opcion(self, obj):
        # Retorna la primera opción asociada al paso
        opcion = Conversacion_Opcion.objects.filter(conversacion_paso=obj).first()
        if opcion:
            return ConversacionOpcionSerializer(opcion).data
        return None

class ConversacionOpcionSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='opcion.nombre', read_only=True)
    respuestas = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion_Opcion
        fields = ['conversacion_opcion_id', 'nombre', 'respuestas']

    def get_respuestas(self, obj):
        respuestas = Respuesta.objects.filter(opcion=obj.opcion)
        if respuestas.exists():
            return RespuestaSerializer(respuestas, many=True).data
        return []

class ConversacionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion_Respuesta
        fields = ['conversacion_respuesta_id', 'respuesta']
