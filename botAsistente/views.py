# path chat/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime    

from conversaciones.models import Conversacion

from .utils import (
    iniciar_conversacion,
    listar_conversaciones_anteriores,
    listar_tipo_gestiones,
    seleccionar_tipo_gestion,
    listar_gestiones,
    seleccionar_gestion,
    listar_opciones,
    seleccionar_opcion,
    listar_respuestas,
    avanzar_paso,
    cerrar_conversaciones_abiertas
)

class ConversacionView(APIView):
    def get(self, request, *args, **kwargs):
        return listar_conversaciones_anteriores(request)
    
    def post(self, request):
        return iniciar_conversacion(request)
    
class TipoGestionView(APIView):
    def get(self, request):
        return listar_tipo_gestiones()
    
    def post(self, request):
        return seleccionar_tipo_gestion(request)

class GestionView(APIView):
    def get(self, request, tipo_gestion_id=None):
        if tipo_gestion_id:
            return listar_gestiones(tipo_gestion_id)
        else:
            return Response({"error": "El parámetro 'tipo_gestion_id' es requerido."}, status=400)

    def post(self, request):
        return seleccionar_gestion(request)
    
class PasoView(APIView):
    def post(self, request):
        return avanzar_paso(request)
    
class OpcionView(APIView):
    def get(self, request):     
        return listar_opciones()
             
    def post(self, request):
        return seleccionar_opcion(request)
    
class RespuestaView(APIView):
    def get(self, request):
        return listar_respuestas()
    
class CerrarConversacion(APIView):
    def post(self, request):
        return cerrar_conversaciones_abiertas()