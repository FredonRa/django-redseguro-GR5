# tipoGestiones/views.py
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from .models import Tipo_Gestion
from .serializers import TipoGestionesSerializer

class TipoGestionesViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Gestion.objects.all()
    serializer_class = TipoGestionesSerializer
    
    def get(self, request):
        tipoGestiones = Tipo_Gestion.objects.filter()
        preguntasFrecuentes_serializadas = TipoGestionesSerializer(tipoGestiones, many=True).data
        return JsonResponse(preguntasFrecuentes_serializadas, status=status.HTTP_200_OK, safe=False)