# usuario/urls.py
from django.urls import path
from .views import PreguntaFrecuenteViewSet

urlpatterns = [
    path('api/preguntasFrecuentes/', PreguntaFrecuenteViewSet.as_view({'get': 'get'}), name='get'),
]