# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, index,login_view

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('api/', include(router.urls)),
    path('registro/', index, name="index"),
    path('ingresar/', login_view, name="login"),
    path('api/login/', login_view, name="login"), 


]