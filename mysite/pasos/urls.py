from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('conversaciones.urls')),
    path('api/', include('gestiones.urls')),
    path('api/', include('pasos.urls')),
]