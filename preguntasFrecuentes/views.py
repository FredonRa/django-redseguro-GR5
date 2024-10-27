# preguntasFrecuentes/views.py
from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .models import PreguntaFrecuente
from .serializers import PreguntaFrecuenteSerializer

class PreguntaFrecuenteViewSet(viewsets.ViewSet):
    serializer_class = PreguntaFrecuenteSerializer
    
    def index(self, request):
        return render(request, "preguntasFrecuentes.html")
    
    def get(self, request):
        preguntasFrecuentes = PreguntaFrecuente.objects.filter(activo=True)
        print(preguntasFrecuentes)
        preguntasFrecuentes_serializadas = PreguntaFrecuenteSerializer(preguntasFrecuentes, many=True).data
        
        return JsonResponse(preguntasFrecuentes_serializadas, status=status.HTTP_200_OK, safe=False)