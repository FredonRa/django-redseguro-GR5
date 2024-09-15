# usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .exceptions import NombreError, ApellidoError, EmailError, ContraseniaError, EmailNotUniqueError
from django.shortcuts import render

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Lógica para validar los campos
            data = request.data
            serializer = self.get_serializer(data=data)
            
            if not data.get('nombre'):
                raise NombreError('El campo nombre es obligatorio.')
            if not data.get('apellido'):
                raise ApellidoError('El campo apellido es obligatorio.')
            if not data.get('email'):
                raise EmailError('El campo email es obligatorio.')
            if Usuario.objects.filter(email=data.get('email')).exists():
                raise EmailNotUniqueError('El email ingresado ya está en uso.')
            if not data.get('contrasenia') or len(data.get('contrasenia')) < 7:
                raise ContraseniaError('La contraseña debe tener al menos 7 caracteres.')
            
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer) 
            
            return Response({
                'message': 'Usuario actualizado exitosamente.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
             
        except NombreError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except ApellidoError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except EmailError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except ContraseniaError as e:
            return Response({'message': str(e)}, status=e.status_code)
        except Exception as e:
            return Response({'message': 'Ocurrió un problema con el servidor, vuelva a intentar en unos minutos.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def index (req):
    return render(req, "registro.html")