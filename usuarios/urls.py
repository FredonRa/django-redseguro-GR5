# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, AuthViewSet

# Crear el router para las vistas de usuarios
# router = DefaultRouter()
# router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

# Definir las rutas

urlpatterns = [
    # Rutas para la API
    path('api/usuarios/', UsuarioViewSet.as_view({'post': 'post'}), name='crear-usuario'),  # Método POST para crear usuario
    path('api/usuarios/actualizar/', UsuarioViewSet.as_view({'patch': 'patch'}), name='modificar_usuario'),
    path('api/usuarios/cambiar-contrasenia/', UsuarioViewSet.as_view({'patch': 'patch_password'}), name='cambiar_contrasenia'),
    
    # Rutas para la vista de autenticación y gestión de cuenta
    path('', AuthViewSet.as_view({'get': 'home'}), name='home'),
    path('registro/', AuthViewSet.as_view({'get': 'index'}), name='registro'),
    path('ingresar/', AuthViewSet.as_view({'get': 'login'}), name='login'),
    path('cuenta/', AuthViewSet.as_view({'get': 'cuenta'}), name='cuenta'),
    path('actualizarDatos/', AuthViewSet.as_view({'get': 'actualizarDatos'}), name='actualizarDatos'),
    path('modificarContrasenia/', AuthViewSet.as_view({'get': 'modificarContrasenia'}), name='modificarContrasenia'),
    
    # Rutas para la autenticación
    path('auth/', AuthViewSet.as_view({'post': 'auth'}), name='auth'),
    
    # Rutas para la actualización de usuario y cambio de contraseña
    # path('api/usuarios/actualizar/', ActualizarUsuarioViewSet.as_view(), name='actualizar-usuario'),
    # path('api/usuarios/cambiar-contrasenia/', CambiarContraseniaViewSet.as_view({'patch': 'update'}), name='cambiar-contrasenia'),
]
