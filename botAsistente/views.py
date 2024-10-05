# path chat/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime    

from conversaciones.models import Conversacion

from .utils import (
    iniciar_conversacion,
    listar_conversaciones_anteriores,
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
        usuario_id = self.kwargs["usuario_id"]
        return listar_conversaciones_anteriores(usuario_id)
    
    def post(self, request):
        return iniciar_conversacion(request)

class GestionView(APIView):
    def get(self, request):
        return listar_gestiones()

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