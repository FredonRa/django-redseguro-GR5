# conversaciones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversacion
from .serializers import ConversacionSerializer
from django.http import JsonResponse
from django.db import models
from django.db.models import ForeignKey

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
        # Obtén el modelo estáticamente o dinámicamente si se requiere en el futuro
        model = Conversacion
        fields = model._meta.get_fields()
        
        # Formatea los tipos de campo
        field_types = []
        for field in fields:
            field_type = 'datetime-local' if isinstance(field, models.DateTimeField) else \
                         'select' if isinstance(field, models.ForeignKey) else \
                         'number' if isinstance(field, models.IntegerField) else \
                         'text' if isinstance(field, models.CharField) else \
                         'unknown'
            
            field_info = {
                'name': field.name,
                'type': field_type,
                'editable': field.editable and not field.primary_key
            }
            
            # Si el campo es ForeignKey, obtengo las claves del modelo relacionado
            if isinstance(field, ForeignKey):
                related_model = field.related_model
                related_fields = related_model._meta.get_fields()
                
                # Filtra los nombres de los campos de interés (id, nombre y apellido)
                related_field_names = [
                    related_field.name 
                    for related_field in related_fields 
                    if related_field.name in ['usuario_id', 'nombre', 'apellido']
                ]
                field_info['options'] = related_field_names
            
            field_types.append(field_info)
        
        return JsonResponse(field_types, safe=False)


class ModelActionsView(APIView):
    def get(self, request, *args, **kwargs):
        acciones = {
            'crear': True,  # O False según la lógica de negocio
            'editar': True,    # O False según la lógica de negocio
            'eliminar': False   # O False según la lógica de negocio
        }
        return JsonResponse(acciones, safe=False)
