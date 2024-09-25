from django.shortcuts import render, redirect

# Create your views here.
def crud(req):
    # Divide la URL en partes
    path_parts = req.path.split('/')

    # Verifica si hay una entidad en la URL (debería ser el segundo elemento)
    if len(path_parts) < 4 or not path_parts[-2]:  # [-2] es la entidad
        return redirect('conversaciones')  # Redirige a la vista predeterminada

    entity = path_parts[-2]  # Obtiene la entidad de la URL
    context = {
        'entity': entity,  # Puedes usar esto en tu plantilla para mostrar contenido específico
    }
    return render(req, 'crud.admin.html', context)