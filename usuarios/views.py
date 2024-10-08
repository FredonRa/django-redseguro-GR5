# usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .exceptions import NombreError, ApellidoError, EmailError, ContraseniaError, EmailNotUniqueError
from django.shortcuts import render, redirect
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
    
class AuthViewSet(viewsets.ViewSet):
    def home(self, request):
        return render(request, "home.html")
    
    def index(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if(session_id):
            return redirect('/home/')
        return render(request, "registro.html")
    
    def login(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if(session_id):
            return redirect('/home/')
        return render(request, "login.html")
    
    def auth(self, request):
        email = request.data.get('email')
        contrasenia = request.data.get('contrasenia')
        usuario = Usuario.objects.filter(email=email).first()

        if usuario is None:
            return JsonResponse({"message": "Credenciales incorrectas"}, status=401)

        if usuario.contrasenia !=  contrasenia:
            return JsonResponse({"message": "Credenciales incorrectas"}, status=401)

        respuesta = JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)
        respuesta.set_cookie('session_id', usuario.pk, max_age=3600)
        respuesta.set_cookie('username', usuario.nombre, max_age=3600)
        respuesta.set_cookie('email', usuario.email, max_age=3600)
        return respuesta