# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpcionViewSet, OpcionFieldsView, OpcionActionsView

router = DefaultRouter()
router.register(r'opciones', OpcionViewSet, basename='opciones')

urlpatterns = [
    path('opciones/campos/', OpcionFieldsView.as_view(), name='model-fields'),
    path('opciones/acciones/', OpcionActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]