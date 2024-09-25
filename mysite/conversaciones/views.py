# conversaciones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversacion
from .serializers import ConversacionSerializer
from django.http import JsonResponse
from mysite.utils.views import ModelFieldsBaseView, ModelActionsBaseView

class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class ConversacionFieldsView(ModelFieldsBaseView):
    model = Conversacion

class ConversacionActionsView(ModelActionsBaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)