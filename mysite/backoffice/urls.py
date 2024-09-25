from django.urls import path
from . import views

urlpatterns = [
    path('', views.crud, name='home'),
    path('conversaciones/', views.crud, name='conversaciones'),
    path('gestiones/', views.crud, name='gestiones'),
    path('pasos/', views.crud, name='pasos'),
    path('opciones/', views.crud, name='opciones'),
    path('respuestas/', views.crud, name='respuestas'),
]