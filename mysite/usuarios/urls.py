# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, index,LoginView,login,home

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
   # path('api/', include(router.urls)),
    path('registro/', index, name="index"),
    path('ingresar/', login, name="login"),
    path('api/login/', LoginView.as_view() , name="login"), 
    path('home/', home , name="home"),
]