# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversacionViewSet, get_model_field_types

router = DefaultRouter()
router.register(r'conversaciones', ConversacionViewSet, basename='conversaciones')

urlpatterns = [
    path('conversaciones/fields/', get_model_field_types, name='model-fields'),
    path('', include(router.urls)),
]