const UsuarioService = new _UsuarioService();

window.addEventListener('DOMContentLoaded', async function () {
    const formularioDeRegistro = document.getElementById('formulario-de-registro')

    formularioDeRegistro.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const errors = validateFormData(formData);
        const usuario = getFormData(formData);

        if (
            !errors.email.error &&
            !errors.nueva_contrasenia.error
        ) {
            submit(usuario)
        }
    });
})

const submit = async () => {
    const nueva_contrasenia = document.getElementById('nueva_contrasenia').value;  // Obtener la nueva contraseña desde el input

    try {
        const data = await UsuarioService.updatePassword(nueva_contrasenia);
        showAlert("success", "Contraseña actualizada correctamente.");
        window.location.href = "/ingresar/";  // Redirigir al login o a donde corresponda
    } catch (err) {
        console.error(err);
        showAlert("error", "Hubo un error al actualizar la contraseña.");
    }
}

function showError(input, errorInputId) {
    document.getElementById(input).classList.add('ring-red-500', 'focus:ring-red-500'); // Cambiar borde a rojo
    document.getElementById(errorInputId).classList.remove('hidden'); // Mostrar mensaje de error
}

function resetErrors() {
    // Reiniciar todas las clases de error y ocultar mensajes
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('ring-red-500', 'focus:ring-red-500');
    });

    const errorMessages = document.querySelectorAll('span[id$="-text-error"]');
    errorMessages.forEach(span => {
        span.classList.add('hidden');
    });
}

const getFormData = (formData) => {
    const email = formData.get('email');
    const nueva_contrasenia = formData.get('nueva_contrasenia');
    return {email, nueva_contrasenia }
}

const validateFormData = (formData) => {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    // Obtener los valores de los campos
    const {email, nueva_contrasenia } = getFormData(formData);

    const errors = {
        email: {
            error: false,
        },
        nueva_contrasenia: {
            error: false,
        },
    };

    resetErrors();




    // Validar contraseña (ejemplo: al menos 6 caracteres)
    if (!contrasenia.trim() || contrasenia.length < 6) {
        errors.contrasenia.error = true;
        showError("contrasenia", 'contrasenia-text-error');
    }

    return errors;
}

