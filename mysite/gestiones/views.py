from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Gestion
from .serializers import GestionSerializer

class GestionViewSet(viewsets.ModelViewSet):
    queryset = Gestion.objects.all()
    serializer_class = GestionSerializer