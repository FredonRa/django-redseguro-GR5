# usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .exceptions import NombreError, ApellidoError, EmailError, ContraseniaError, EmailNotUniqueError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Lógica para validar los campos
            data = request.data
            serializer = self.get_serializer(data=data)
            
            if not data.get('nombre'):
                raise NombreError('El campo nombre es obligatorio.')
            if not data.get('apellido'):
                raise ApellidoError('El campo apellido es obligatorio.')
            if not data.get('email'):
                raise EmailError('El campo email es obligatorio.')
            if Usuario.objects.filter(email=data.get('email')).exists():
                raise EmailNotUniqueError('El email ingresado ya está en uso.')
            if not data.get('contrasenia') or len(data.get('contrasenia')) < 7:
                raise ContraseniaError('La contraseña debe tener al menos 7 caracteres.')
            
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer) 
            
            return Response({
                'message': 'Usuario actualizado exitosamente.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
             
        except NombreError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except ApellidoError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except EmailError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except ContraseniaError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except Exception as e:
            return Response({'message': 'Ocurrió un problema con el servidor, vuelva a intentar en unos minutos.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def index (req):
    return render(req, "registro.html")
def login (req):
    return render(req, "login.html")

# Create your views here.
# @login_required
# def index (req):
#      return render(req, "index.html")

# def salir(req):
#     logout(req)
#     return redirect('/') 

def login_view(request):
    #if request.method == "POST":
        email = request.POST.get('email')
        contrasenia = request.POST.get('contrasenia')
        #user = authenticate(request, username=username, password=password)
        return JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)
    # if user is not None:
    #          login(request, user)
    # else:
    #          return JsonResponse({"error": "Credenciales inválidas"}, status=400)
    # return render(request, 'login.html')
