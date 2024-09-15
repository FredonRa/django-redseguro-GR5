# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RespuestaViewSet

router = DefaultRouter()
router.register(r'respuestas', RespuestaViewSet, basename='respuestas')

urlpatterns = [
    path('', include(router.urls)),
]