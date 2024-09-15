# usuario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GestionViewSet

router = DefaultRouter()
router.register(r'gestiones', GestionViewSet, basename='gestiones')

urlpatterns = [
    path('', include(router.urls)),
]