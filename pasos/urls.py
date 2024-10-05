from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasoViewSet, PasoFieldsView, PasoActionsView

router = DefaultRouter()
router.register(r'pasos', PasoViewSet , basename='pasos')

urlpatterns = [
    path('pasos/campos/', PasoFieldsView.as_view(), name='model-fields'),
    path('pasos/acciones/', PasoActionsView.as_view(), name='model-actions'),
    path('', include(router.urls)),
]