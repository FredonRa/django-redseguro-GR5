from rest_framework import serializers
from .models import Conversacion, Conversacion_Gestion, Conversacion_Opcion, Conversacion_Paso, Conversacion_Respuesta
from respuestas.models import Respuesta
from respuestas.serializers import RespuestaSerializer

class ConversacionSerializer(serializers.ModelSerializer):
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

class ConversacionGestionSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='gestion.nombre', read_only=True)  # Añadir el nombre de la gestión
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
        opcion = Conversacion_Opcion.objects.filter(conversacion_paso=obj).first()
        if(opcion is None):
            return None
        return ConversacionOpcionSerializer(opcion).data

class ConversacionOpcionSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='opcion.nombre', read_only=True)  # Añadir el nombre de la opción
    respuestas = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion_Opcion
        fields = ['conversacion_opcion_id', 'nombre', 'respuestas']

    def get_respuestas(self, obj):
        respuestas = Respuesta.objects.filter(opcion=obj.opcion)
        if(respuestas.exists()):
            return RespuestaSerializer(respuestas, many=True).data
        return None

class ConversacionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion_Respuesta
        fields = ['conversacion_respuesta_id', 'respuesta']