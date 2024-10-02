# conversaciones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Conversacion
from .serializers import ConversacionSerializer

class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)