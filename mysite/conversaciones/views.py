# conversaciones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Conversacion
from .serializers import ConversacionSerializer
from django.apps import apps
from django.http import JsonResponse
from django.db import models

class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
class ModelFieldsView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener el modelo Conversacion
        try:
            model = apps.get_model('conversaciones', 'Conversacion')
            print("model: ", model)
        except LookupError:
            raise NotFound("Modelo 'Conversacion' no encontrado.")
        
        # Obtener los campos del modelo
        fields = [field.name for field in model._meta.get_fields()]
        
        return Response({'fields': fields}, status=status.HTTP_200_OK)
    
def get_model_field_types(request):
    # Obtén el modelo dinámicamente
    model = apps.get_model('conversaciones', "Conversacion")
    fields = model._meta.get_fields()
    
    # Formatea los tipos de campo
    field_types = []
    for field in fields:
        field_info = {
            'name': field.name,
            'type': 'datetime' if isinstance(field, models.DateTimeField) else 
                    'integer' if isinstance(field, models.IntegerField) else 
                    'char' if isinstance(field, models.CharField) else 
                    'integer' if isinstance(field, models.ForeignKey) else 
                    'other'
        }
        field_types.append(field_info)
    
    return JsonResponse(field_types, safe=False)