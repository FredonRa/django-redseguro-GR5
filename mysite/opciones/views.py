# opciones/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Opcion
from .serializers import OpcionSerializer
from mysite.utils.views import ModelFieldsBaseView, ModelActionsBaseView

class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
class OpcionFieldsView(ModelFieldsBaseView):
    model = Opcion

class OpcionActionsView(ModelActionsBaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)