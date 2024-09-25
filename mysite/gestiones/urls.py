# gestiones/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GestionViewSet, GestionFieldsView, GestionActionsView

router = DefaultRouter()
router.register(r'gestiones', GestionViewSet, basename='gestiones')

urlpatterns = [
    path('gestiones/campos/', GestionFieldsView.as_view(), name='model-fields'),
    path('gestiones/acciones/', GestionActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]