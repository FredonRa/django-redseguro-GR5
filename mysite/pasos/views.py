from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Pasos
from .serializers import PasosSerializer

class PasosViewSet(viewsets.ModelViewSet):
    queryset = Pasos.objects.all()
    serializer_class = PasosSerializer