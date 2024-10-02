from django.shortcuts import render,redirect
from rest_framework import viewsets
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer


# Create your views here.

# Ejemplo de vista basada en clases para el ViewSet de Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Ejemplo de vistas basadas en funciones
def index(request):
    return render(request, 'index.html')

def salir(request):
    # Lógica para cerrar sesión
    return redirect('index')

def login_view(request):
    # Lógica para iniciar sesión
    return render(request, 'login.html')
