# mysite/utils/views/views.py
from django.http import JsonResponse
from django.db import models
from django.db.models import ForeignKey
from rest_framework.views import APIView

class ModelFieldsBaseView(APIView):
    model = None

    def get(self, request, *args, **kwargs):
        if self.model is None:
            return JsonResponse({'error': 'Model not specified'}, status=400)

        fields = self.model._meta.get_fields()

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
                'editable': field.editable and not field.primary_key,
                'null': field.null
            }

            if isinstance(field, ForeignKey):
                related_model = field.related_model
                related_fields = related_model._meta.get_fields()

                related_field_names = [
                    related_field.name 
                    for related_field in related_fields 
                    if related_field.name in ['usuario_id', 'gestion_id', 'opcion_id', 'paso_id', 'nombre', 'apellido']
                ]
                field_info['options'] = related_field_names

            field_types.append(field_info)

        return JsonResponse(field_types, safe=False)


class ModelActionsBaseView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear = False
        self.editar = False
        self.eliminar = False
    
    def get_actions(self):
        """
        Sobrescribe esta función en las subclases para definir la lógica de acciones específicas.
        """
        return {
            'crear': self.crear,   # Valor por defecto o lógica de negocio general
            'editar': self.editar,  # Valor por defecto o lógica de negocio general
            'eliminar': self.eliminar # Valor por defecto o lógica de negocio general
        }

    def get(self, request, *args, **kwargs):
        acciones = self.get_actions()
        return JsonResponse(acciones, safe=False)