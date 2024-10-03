from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef

from conversaciones.models import Conversacion, Conversacion_Gestion, Conversacion_Paso, Conversacion_Opcion
from usuarios.models import Usuario
from gestiones.models import Gestion
from pasos.models import Paso
from opciones.models import Opcion
from respuestas.models import Respuesta

from conversaciones.serializers import ConversacionSerializer, ConversacionGestionSerializer
from gestiones.serializers import GestionSerializer
from opciones.serializers import OpcionSerializer
from respuestas.serializers import RespuestaSerializer

def conversacion_existente(conversacion_existente):
    # Serializar la conversación principal
    conversacion_data = ConversacionSerializer(conversacion_existente).data
    
    # Obtener la gestión relacionada a la conversación (solo una)
    gestion = Conversacion_Gestion.objects.filter(conversacion=conversacion_existente.conversacion_id).first()
    
    # Si hay una gestión, serializarla; si no, devolver None
    if gestion:
        gestion_data = ConversacionGestionSerializer(gestion).data
    else:
        gestion_data = None

    # Agregar la gestión a la respuesta
    conversacion_data['gestion'] = gestion_data
    return conversacion_data

def listar_conversaciones_anteriores(usuario_id):
    # Obtener las conversaciones anteriores del usuario 
    conversaciones_anteriores  = Conversacion.objects.filter(usuario=usuario_id, fecha_fin__isnull=False)
    
    # Lista para almacenar las conversaciones serializadas
    conversaciones_data = []

    for conversacion in conversaciones_anteriores:
        # Llamar al método conversacion_existente para serializar cada conversación
        response = conversacion_existente(conversacion)
        
        # Extraer el contenido de la respuesta
        conversaciones_data.append(response)

    return Response(conversaciones_data, status=200)

def iniciar_conversacion(request):
    """
    Inicia una nueva conversación, recibiendo usuario_id en el cuerpo de la solicitud.
    """
    usuario_id = request.data.get('usuario')

    if not usuario_id:
        return Response({'error': 'usuario_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el usuario existe
    try:
        usuario = Usuario.objects.get(usuario_id=usuario_id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Verificar si el usuario ya tiene una conversación activa (sin fecha_fin)
    conversacion_abierta = Conversacion.objects.filter(usuario=usuario, fecha_fin__isnull=True).first()

    if conversacion_abierta:
        return Response(conversacion_existente(conversacion_abierta), status=200)

    # Si no hay conversaciones abiertas, crear una nueva conversación
    conversacion = Conversacion.objects.create(usuario=usuario)

    return Response({
        'mensaje': 'Conversación iniciada',
        'conversacion_id': conversacion.conversacion_id,
        'usuario_id': usuario_id
    }, status=status.HTTP_201_CREATED)

def listar_gestiones():
    """
    Envía las gestiones disponibles que tienen opciones con al menos una respuesta.
    """
    gestiones = Gestion.objects.filter(
        Exists(
            Paso.objects.filter(gestion=OuterRef('pk')).filter(
                Exists(
                    Opcion.objects.filter(paso=OuterRef('pk')).filter(
                        Exists(
                            Respuesta.objects.filter(opcion=OuterRef('pk'))
                        )
                    )
                )
            )
        )
    )

    gestiones_serializadas = GestionSerializer(gestiones, many=True).data

    return Response({'gestiones': gestiones_serializadas}, status=status.HTTP_200_OK)
    
def seleccionar_gestion(request):
    """
    Con la gestión seleccionada, iniciar el primer paso de la conversación y enviar opciones.
    """
    # conversacion_id = request.data.get('conversacion_id')
    gestion_id = request.data.get('gestion_id')
    conversacion_abierta = Conversacion.objects.filter(conversacion_id=86, fecha_fin__isnull=True).first()
    conversacion_id = conversacion_abierta.conversacion_id
    if not conversacion_id or not gestion_id:
        return Response({'error': 'conversacion_id y gestion_id son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    conversacion = get_object_or_404(Conversacion, conversacion_id=conversacion_id)

    # Verificar si ya hay una gestión activa en la conversación (sin fecha_fin)
    gestion_activa = Conversacion_Gestion.objects.filter(conversacion=conversacion_abierta).first()

    if gestion_activa:
        return Response({
            'error': 'Esta conversación ya tiene una gestión activa',
            'gestion_id': gestion_activa.gestion.gestion_id
        }, status=status.HTTP_400_BAD_REQUEST)

    # Si no hay una gestión activa, crear una nueva gestión para la conversación
    conversacion_gestion = Conversacion_Gestion.objects.create(
        conversacion=conversacion,
        gestion_id=gestion_id
    )

    # Obtener el primer paso de la gestión
    primer_paso = Paso.objects.filter(gestion_id=gestion_id).order_by('orden').first()
    if primer_paso:
        Conversacion_Paso.objects.create(
            conversacion_gestion=conversacion_gestion,
            paso=primer_paso
        )
        return obtener_opciones(conversacion_gestion.conversacion_gestion_id, primer_paso)

    return Response({'mensaje': 'No se encontraron pasos para esta gestión'}, status=status.HTTP_404_NOT_FOUND)


def obtener_opciones(conversacion_gestion_id, paso):
    """
    Obtiene las opciones para el paso actual de la conversación.
    """
    conversacion_paso = Conversacion_Paso.objects.filter(
        conversacion_gestion_id=conversacion_gestion_id,
        paso=paso
    ).first()

    if not conversacion_paso:
        return Response({'mensaje': 'No hay pasos disponibles en esta gestión'}, status=status.HTTP_404_NOT_FOUND)

    opciones = Opcion.objects.filter(paso=paso)
    opciones_serializadas = OpcionSerializer(opciones, many=True)

    return Response({
        'paso_actual': conversacion_paso.paso.paso_id,
        'conversacion_gestion_id': conversacion_gestion_id,
        'opciones': opciones_serializadas.data
    }, status=status.HTTP_200_OK)
    
def listar_opciones():
    """
    Envía las gestiones disponibles (ya guardadas en la base de datos)
    que tengan al menos una respuesta.
    """
    opciones = Opcion.objects.filter(
        Exists(
            Respuesta.objects.filter(opcion=OuterRef('pk'))
        )
    )

    opciones_serializadas = OpcionSerializer(opciones, many=True).data
    return Response({'opciones': opciones_serializadas}, status=status.HTTP_200_OK)

def listar_respuestas():
    """
    Envía las gestiones disponibles (ya guardadas en la base de datos).
    """
    respuestas = Respuesta.objects.all()
    respuestas_serializadas = RespuestaSerializer(respuestas, many=True).data
    return Response({'respuestas': respuestas_serializadas}, status=status.HTTP_200_OK)

def seleccionar_opcion(request):
    """
    Maneja la selección de una opción dentro del paso actual.
    """
    conversacion_gestion_id = request.data.get('conversacion_gestion_id')
    opcion_id = request.data.get('opcion_id')
    paso_id = request.data.get('paso_id')

    conversacion_paso = get_object_or_404(Conversacion_Paso, conversacion_gestion=conversacion_gestion_id, paso=paso_id)
    opcion = get_object_or_404(Opcion, opcion_id=opcion_id)

    Conversacion_Opcion.objects.create(conversacion_paso=conversacion_paso, opcion_id=opcion.opcion_id)
    
    respuestas_opcion = Respuesta.objects.filter(opcion=opcion.opcion_id)

    if respuestas_opcion.exists():
        respuestas_serializadas = RespuestaSerializer(respuestas_opcion, many=True)
        finalizar_conversacion(conversacion_paso.conversacion_gestion.conversacion.conversacion_id)
        return Response({
            'mensaje': 'Conversación finalizada', 
            'respuestas': respuestas_serializadas.data
        })

    siguiente_paso = opcion.siguiente_paso
    
    if siguiente_paso:
        avanzar_paso(conversacion_paso.conversacion_gestion, siguiente_paso)
        return obtener_opciones(conversacion_paso.conversacion_gestion.conversacion_gestion_id, siguiente_paso)

    return Response({'mensaje': 'No hay siguiente paso'}, status=status.HTTP_200_OK)


def finalizar_conversacion(conversacion_id):
    """
    Marca una conversación como finalizada, estableciendo la fecha de finalización.
    """
    Conversacion.objects.filter(conversacion_id=conversacion_id).update(fecha_fin=timezone.now())


def avanzar_paso(conversacion_gestion, paso):
    """
    Avanza al siguiente paso dentro de la conversación.
    """
    Conversacion_Paso.objects.create(conversacion_gestion=conversacion_gestion, paso=paso)

def cerrar_conversaciones_abiertas():
    """
    Cierra todas las conversaciones que están abiertas (sin fecha_fin).
    """
    conversaciones_abiertas = Conversacion.objects.filter(fecha_fin__isnull=True)

    if not conversaciones_abiertas.exists():
        return Response({'mensaje': 'No hay conversaciones abiertas'}, status=status.HTTP_404_NOT_FOUND)

    # Actualizar todas las conversaciones abiertas con la fecha actual
    conversaciones_abiertas.update(fecha_fin=timezone.now())

    return Response({'mensaje': f'Se cerraron {conversaciones_abiertas.count()} conversaciones abiertas.'}, status=status.HTTP_200_OK)