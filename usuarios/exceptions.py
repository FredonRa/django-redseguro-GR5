from rest_framework.exceptions import APIException

class NombreError(APIException):
    status_code = 400
    default_detail = 'Error en el campo nombre.'
    default_code = 'nombre_error'

class ApellidoError(APIException):
    status_code = 400
    default_detail = 'Error en el campo apellido.'
    default_code = 'apellido_error'

class EmailError(APIException):
    status_code = 400
    default_detail = 'Error en el campo email.'
    default_code = 'email_error'
    
class EmailNotUniqueError(EmailError):
    default_detail = 'El email ingresado ya está en uso.'

class ContraseniaError(APIException):
    status_code = 400
    default_detail = 'Error en el campo contraseña.'
    default_code = 'contrasenia_error'