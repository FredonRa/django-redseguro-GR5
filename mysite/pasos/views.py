from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Paso
from .serializers import PasoSerializer

class PasoViewSet(viewsets.ModelViewSet):
    queryset = Paso.objects.all()
    serializer_class = PasoSerializer