from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasosViewSetViewSet

router = DefaultRouter()
router.register(r'pasos', PasosViewSetViewSet , basename='pasos')

urlpatterns = [
    path('', include(router.urls)),
]