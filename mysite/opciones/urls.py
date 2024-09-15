# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpcionViewSet

router = DefaultRouter()
router.register(r'opciones', OpcionViewSet, basename='opciones')

urlpatterns = [
    path('', include(router.urls)),
]