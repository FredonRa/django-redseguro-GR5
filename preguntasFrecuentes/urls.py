# usuario/urls.py
from django.urls import path
from .views import PreguntaFrecuenteViewSet

urlpatterns = [
    path('preguntas-frecuentes/', PreguntaFrecuenteViewSet.as_view({'get': 'index'}), name='index'),
    path('api/preguntasFrecuentes/', PreguntaFrecuenteViewSet.as_view({'get': 'get'}), name='get'),
]