# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, AuthViewSet

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuarios')


urlpatterns = [
    path('api/', include(router.urls)),
    path('registro/', AuthViewSet.as_view({'get': 'index'}), name='index'),
    path('', AuthViewSet.as_view({'get': 'home'}), name='home'),
    path('actualizarDatos/', AuthViewSet.as_view({'get': 'actualizarDatos'}), name='actualizarDatos'),
    path('ingresar/', AuthViewSet.as_view({'get': 'login'}), name='login'),
    path('auth/', AuthViewSet.as_view({'post': 'auth'}), name='auth'),
]