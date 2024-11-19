from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .exceptions import NombreError, ApellidoError, EmailError, ContraseniaError, EmailNotUniqueError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets, mixins

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

class UsuarioViewSet(viewsets.ViewSet):
    def post(self, request):
        """
        Crea un nuevo usuario.
        Este método no requiere autenticación.
        """
        data = request.data  # Los datos de la petición

        first_name = data.get('nombre')
        last_name = data.get('apellido')
        email = data.get('email')
        password = data.get('contrasenia')

        # Validación básica de los campos
        if not first_name or not last_name or not email or not password:
            return Response(
                {"message": "Todos los campos son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "El correo electrónico ya está en uso."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 7:
            return Response(
                {"message": "La contraseña debe tener al menos 7 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el usuario
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        return Response(
            {"message": "Usuario creado exitosamente."},
            status=status.HTTP_201_CREATED
        )
    
    def patch(self, request):
        """
        Actualiza los datos del usuario autenticado.
        """
        user = request.user
        data = request.data
        
        # Actualizamos los datos personales
        user.first_name = data.get('nombre', user.first_name)
        user.last_name = data.get('apellido', user.last_name)
        user.email = data.get('email', user.email)  # Actualiza email si es necesario
        
        try:
            user.save()
            respuesta = Response({"message": "Datos actualizados correctamente."}, status=status.HTTP_200_OK)
            respuesta.set_cookie('username', user.first_name, max_age=3600)
            respuesta.set_cookie('lastname', user.last_name, max_age=3600)
            return respuesta
        except Exception as e:
            return Response({"error": "No se pudieron actualizar los datos.", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch_password(self, request):
        """
        Actualiza solo la contraseña del usuario autenticado.
        """
        user = request.user
        data = request.data
        
        contrasenia_actual = data.get('contraseniaActual')
        contrasenia_nueva = data.get('contraseniaNueva')
        
        if not contrasenia_actual or not contrasenia_nueva:
            return Response({"error": "Ambas contraseñas son requeridas."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si la contraseña actual es correcta
        if not user.check_password(contrasenia_actual):
            return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que la nueva contraseña sea diferente de la actual
        if contrasenia_actual == contrasenia_nueva:
            return Response({"error": "La nueva contraseña no puede ser igual a la actual."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar longitud mínima de la nueva contraseña
        if len(contrasenia_nueva) < 7:
            return Response({"error": "La nueva contraseña debe tener al menos 7 caracteres."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar la contraseña
        user.set_password(contrasenia_nueva)
        user.save()
        return Response({"message": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)

# class ActualizarUsuarioViewSet(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user = request.user
#         data = request.data

#         # Actualizar los datos personales
#         user.first_name = data.get('first_name', user.first_name)
#         user.last_name = data.get('last_name', user.last_name)

#         try:
#             user.save()
#             return Response({"message": "Datos actualizados correctamente."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": "No se pudieron actualizar los datos."}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthViewSet(viewsets.ViewSet):
    def home(self, request):
        return render(request, "home.html")
    
    def index(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if session_id:
            return redirect('/')
        return render(request, "registro.html")
    
    def login(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if session_id:
            return redirect('/')
        return render(request, "login.html")
    
    def cuenta(self, request):
        cookies = request.COOKIES
        session_id = cookies.get('session_id')
        if session_id:
            return render(request, "perfil.html")
        return redirect('/')
    
    def auth(self, request):
        email = request.data.get('email')
        contrasenia = request.data.get('contrasenia')
        
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
