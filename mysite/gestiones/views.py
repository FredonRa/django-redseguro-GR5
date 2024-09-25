# gestiones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Gestion
from .serializers import GestionSerializer
from django.http import JsonResponse
from django.db import models
from mysite.utils.views import ModelFieldsBaseView, ModelActionsBaseView


class GestionViewSet(viewsets.ModelViewSet):
    queryset = Gestion.objects.all()
    serializer_class = GestionSerializer
    
class GestionFieldsView(ModelFieldsBaseView):
    model = Gestion
    
class GestionActionsView(ModelActionsBaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes habilitar las acciones necesarias
        self.crear = True
        self.editar = True