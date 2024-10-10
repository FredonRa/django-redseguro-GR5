# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversacionViewSet, ConversacionFieldsView, ConversacionActionsView

router = DefaultRouter()
router.register(r'conversaciones', ConversacionViewSet, basename='conversaciones')

urlpatterns = [
    path('conversaciones/campos/', ConversacionFieldsView.as_view(), name='model-fields'),
    path('conversaciones/acciones/', ConversacionActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]