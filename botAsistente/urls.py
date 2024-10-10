# path chat/urls.py
from django.urls import path
from .views import ConversacionView, GestionView, OpcionView, PasoView, RespuestaView, CerrarConversacion

urlpatterns = [
     path('bot/conversacion/anteriores/', ConversacionView.as_view(), name='listar_conversaciones_anteriores'),
     path('bot/conversacion/iniciar/', ConversacionView.as_view(), name='iniciar_conversacion'),
     # path('bot/conversacion/finalizar/', ConversacionView.as_view(), name='iniciar_conversacion'),
     path('bot/gestiones/', GestionView.as_view(), name='listar_gestiones'),
     path('bot/gestiones/seleccionar_gestion/', GestionView.as_view(), name='seleccionar_gestion'),
     path('bot/opciones/', OpcionView.as_view(), name='listar_opciones'),
     path('bot/opciones/seleccionar_opcion/', OpcionView.as_view(), name='seleccionar_opcion'),
     path('bot/respuestas/', RespuestaView.as_view(), name='listar_respuestas'),
     path('bot/avanzar_paso/', PasoView.as_view(), name='avanzar_paso'),
     path('bot/finalizar/all/', CerrarConversacion.as_view(), name='avanzar_paso'),
]