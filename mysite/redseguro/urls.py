# redseguro/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, index, salir, login_view

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', index, name='index'),
    path('salir/', salir, name='salir'),
    path('login/', login_view, name='login'),
]
