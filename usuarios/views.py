# usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .exceptions import NombreError, ApellidoError, EmailError, ContraseniaError, EmailNotUniqueError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Lógica para validar los campos
            data = request.data
            first_name = data.get('nombre')
            last_name = data.get('apellido')
            password = data.get('contrasenia')
            email = data.get('email')
            
            if not first_name:
                raise NombreError('El campo nombre es obligatorio.')
            if not last_name:
                raise ApellidoError('El campo apellido es obligatorio.')
            if not email:
                raise EmailError('El campo email es obligatorio.')
            if User.objects.filter(email=email).exists():
                raise EmailNotUniqueError('El email ingresado ya está en uso.')
            if not password or len(password) < 7:
                raise ContraseniaError('La contraseña debe tener al menos 7 caracteres.')
            
            User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            
            return Response({
                'message': 'Usuario actualizado exitosamente.',
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
        
    def update(self, request, *args, **kwargs):
        try:
            # Obtener el email del usuario desde los datos del request
            email = request.data.get('email')
            print('HOLAqqqq')

            if not email:
                raise EmailError('El campo email es obligatorio.')

            # Buscar el usuario por su email
            user = User.objects.get(email=email)

            # Obtener los otros datos del request
            first_name = request.data.get('nombre')
            last_name = request.data.get('apellido')

            # Validaciones de campos obligatorios
            if not first_name:
                raise NombreError('El campo nombre es obligatorio.')
            if not last_name:
                raise ApellidoError('El campo apellido es obligatorio.')
            
            # Verificar que el email no esté en uso por otro usuario
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise EmailNotUniqueError('El email ingresado ya está en uso.')

            # Actualizar los campos del usuario
            user.first_name = first_name
            user.last_name = last_name
            
            user.save()  # Guardar los cambios en la base de datos

            response =  Response({
                'message': 'Usuario actualizado exitosamente.',
            }, status=status.HTTP_200_OK)
        
             # Actualizar las cookies
            response.set_cookie('username', user.first_name, max_age=3600)
            response.set_cookie('lastname', user.last_name, max_age=3600)
             
            return response 

        except NombreError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except ApellidoError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except EmailError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except Exception as e:
            return Response ({
                'message': 'Ocurrió un problema con el servidor, vuelva a intentar en unos minutos.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['post'])   
    def updatePassword(self, request):
            # Extraer nueva contraseña del request
            nueva_contrasenia = request.data.get('nueva_contrasenia')
            print('2123as')
            # Verificar si la nueva contraseña está presente
            if not nueva_contrasenia:
                return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el usuario logueado desde la sesión
            user = request.user

            # Actualizar la contraseña
            user.set_password(nueva_contrasenia)  # Se usa set_password para asegurar que se encripte la contraseña
            user.save()

            return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

class AuthViewSet(viewsets.ViewSet):
    def home(self, request):
        return render(request, "home.html")
    
    def index(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if(session_id):
            return redirect('/')
        return render(request, "registro.html")
    
    def login(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if(session_id):
            return redirect('/')
        return render(request, "login.html")
    

    def actualizarDatos(self,request):
        # Renderizar la página con los datos del usuario
        return render(request, "ActualizarDatos.html", {
        'username':request.COOKIES.get('username'),
        'lastname':request.COOKIES.get('lastname'),
        'email':request.COOKIES.get('email'), 
    })
    
    def modificarContrasenia(self,request):
        # Renderizar la página con los datos del usuario
        return render(request, "modificarContrasenia.html")
    
    def auth(self, request):
        email = request.data.get('email')
        contrasenia = request.data.get('contrasenia')
        # usuario = Usuario.objects.filter(email=email).first()
        usuario = authenticate(request, username=email, password=contrasenia)


        if usuario is None:
            return JsonResponse({"message": "Credenciales incorrectas"}, status=401)

        login(request, usuario)

        respuesta = JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)
        respuesta.set_cookie('session_id', usuario.pk, max_age=3600)
        respuesta.set_cookie('username', usuario.first_name, max_age=3600)
        respuesta.set_cookie('lastname', usuario.last_name, max_age=3600)
        respuesta.set_cookie('email', usuario.email, max_age=3600)
        return respuesta