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
            !errors.contrasenia.error
        ) {
            submit(usuario)
        }
    });
})

const submit  = async (usuario) => {
    await UsuarioService.updatePassword(usuario)
        .then(data => {
            showAlert("success", "Usuario actualizado correctamente.")
            window.location.href = "/ingresar"
            return data
        })
        .catch(err => {
            console.error(err)
            
        });
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
    const contrasenia = formData.get('contrasenia');
    return {email, contrasenia }
}

const validateFormData = (formData) => {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    // Obtener los valores de los campos
    const {email, contrasenia } = getFormData(formData);

    const errors = {
        email: {
            error: false,
        },
        contrasenia: {
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
