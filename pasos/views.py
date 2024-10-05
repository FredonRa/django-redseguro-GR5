# Create your views here.
from rest_framework import viewsets
from .models import Paso
from .serializers import PasoSerializer
from mysite.utils.views import ModelFieldsBaseView, ModelActionsBaseView

class PasoViewSet(viewsets.ModelViewSet):
    queryset = Paso.objects.all()
    serializer_class = PasoSerializer

class PasoFieldsView(ModelFieldsBaseView):
    model = Paso

class PasoActionsView(ModelActionsBaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear = True
        self.editar = True
        self.eliminar = True