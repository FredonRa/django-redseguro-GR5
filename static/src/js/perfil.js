// Instanciar UsuarioService
const UsuarioService = new _UsuarioService();

let loading = false;

// Asegurarse de que el DOM esté completamente cargado antes de configurar los event listeners
document.addEventListener('DOMContentLoaded', () => {
    const nombreInput = document.getElementById('nombre');
    const apellidoInput = document.getElementById('apellido');
    const emailInput = document.getElementById('email');

    const nombre = getCookie('username');
    const apellido = getCookie('lastname');
    const email = getCookie('email');

    nombreInput.value = nombre.replaceAll('"', "")
    apellidoInput.value = apellido.replaceAll('"', "")
    emailInput.value = email.replaceAll('"', "")

    setupEventListeners();

});

// Función para manejar el submit del formulario de datos personales
const handlePersonalDataSubmit = async (event) => {
    event.preventDefault();
    loading = true;
    // Recopilar los datos del formulario
    const nombre = document.getElementById('nombre').value;
    const apellido = document.getElementById('apellido').value;
    const email = document.getElementById('email').value;

    // Crear el objeto de datos
    const data = {
        nombre,
        apellido,
        email,
    };

    toggleButtonState("formulario-de-datos-submit");

    try {
        // Enviar los datos al servicio de actualización de usuario
        const response = await UsuarioService.updateUsuario(data);
        showAlert("success", response.message);
        setTimeout(() => {
            window.location.reload();
        }, 1500)
    } catch (error) {
        showAlert("error", 'Ocurrió un error al actualizar los datos. Por favor, intente nuevamente.');
    } finally {
        // Rehabilitar el botón y ocultar el indicador de carga
        loading = false;
        toggleButtonState("formulario-de-datos-submit");
    }
};

// Función para manejar el submit del formulario de cambiar contraseña
const handleChangePasswordSubmit = async (event) => {
    event.preventDefault();
    loading = true;
    // Recopilar los datos del formulario de cambiar contraseña
    const contraseniaActual = document.getElementById('contrasenia-actual').value;
    const contraseniaNueva = document.getElementById('contrasenia-nueva').value;
    const email = document.getElementById('email').value;

    // Crear el objeto de datos
    const data = {
        contraseniaActual,
        contraseniaNueva,
        email
    };

    toggleButtonState("formulario-de-contrasenia-submit");

    try {
        // Enviar los datos al servicio de actualización de contraseña
        const response = await UsuarioService.updatePassword(data);
        showAlert("success", response.message);
        setTimeout(() => {
            window.location.reload();
        }, 1500)
    } catch (error) {
        showAlert("error", error.message);
    } finally {
        // Rehabilitar el botón y ocultar el indicador de carga
        loading = false;
        toggleButtonState("formulario-de-contrasenia-submit");
    }
};

// Función para agregar los event listeners a los formularios
const setupEventListeners = () => {
    const personalDataForm = document.getElementById('formulario-de-datos');
    const changePasswordForm = document.getElementById('formulario-de-contrasenia');

    // Verificar si los formularios existen antes de agregar los event listeners
    if (personalDataForm) {
        personalDataForm.addEventListener('submit', handlePersonalDataSubmit);
    }

    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', handleChangePasswordSubmit);
    }
};

function toggleButtonState(buttonId) {
    const submitButton = document.getElementById(buttonId);
    if (loading) {
        submitButton.disabled = true;
        submitButton.innerHTML = `<span class="loader"></span> Guardando...`; // Cambiar texto y añadir loader
    } else {
        submitButton.disabled = false;
        submitButton.innerHTML = "Guardar";
    }
}
