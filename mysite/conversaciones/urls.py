# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversacionViewSet, ModelFieldsView, ModelActionsView

router = DefaultRouter()
router.register(r'conversaciones', ConversacionViewSet, basename='conversaciones')

urlpatterns = [
    path('conversaciones/campos/', ModelFieldsView.as_view(), name='model-fields'),
    path('conversaciones/acciones/', ModelActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]