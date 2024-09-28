# path chat/urls.py
from django.urls import path
from .views import ConversacionView, GestionView, OpcionView, PasoView, CerrarConversacion

urlpatterns = [
     path('conversacion/iniciar/', ConversacionView.as_view(), name='iniciar_conversacion'),
     path('conversacion/gestiones/', GestionView.as_view(), name='listar_gestiones'),
     path('conversacion/gestiones/seleccionar_gestion/', GestionView.as_view(), name='seleccionar_gestion'),
     path('conversacion/opciones/seleccionar_opcion/', OpcionView.as_view(), name='seleccionar_opcion'),
     path('conversacion/avanzar_paso/', PasoView.as_view(), name='avanzar_paso'),
     path('conversacion/finalizar/all/', CerrarConversacion.as_view(), name='avanzar_paso'),
]