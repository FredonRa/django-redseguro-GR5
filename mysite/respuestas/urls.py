# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RespuestaViewSet, RespuestaFieldsView, RespuestaActionsView

router = DefaultRouter()
router.register(r'respuestas', RespuestaViewSet, basename='respuestas')

urlpatterns = [
    path('respuestas/campos/', RespuestaFieldsView.as_view(), name='model-fields'),
    path('respuestas/acciones/', RespuestaActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]