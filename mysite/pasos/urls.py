from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasoViewSet

router = DefaultRouter()
router.register(r'pasos', PasoViewSet , basename='pasos')

urlpatterns = [
    path('', include(router.urls)),
]