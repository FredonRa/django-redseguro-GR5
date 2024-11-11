document.addEventListener('DOMContentLoaded', function () {
    // Obtener la cookie
    const userInfoCookie = getCookie('session_id');

    if (userInfoCookie) {
        const usernameCookie = getCookie('username');
        const avatarImage = document.querySelector('#logged-user img');
        const username = document.querySelector('#logged-user #username');
        const profileDropdown = document.getElementById('logged-user');
        const loginUser = document.getElementById('login-user');

        // Actualizar el avatar
        // avatarImage.src = userInfo.avatarUrl;
        avatarImage.src = femaleIcon

        // Mostrar el menú de usuario
        profileDropdown.classList.remove('hidden');

        // Esconder el boton de login
        loginUser.classList.add('hidden');

        // Rellenar el username
        username.textContent = `Hola ${usernameCookie}!`;
    }
});

function login() {
    window.location.href = "/ingresar/"
}

function signup() {
    window.location.href = "/registro/"
}

function logout() {
    //borrando cookies
    deleteCookie('session_id');
    deleteCookie('email');
    deleteCookie('username');
    // Redirigir a la página de ingresar
    window.location.href = "/ingresar/"
}

function actualizarDatos() {

    // Redirigir a la página de actualización de datos
    window.location.href = "/actualizarDatos/";
}



function toggleDropdown() {
    // Obtener el elemento por su ID
    var dropdown = document.getElementById("profile-dropdown");

    // Hacer toggle de la clase 'hidden'
    if (dropdown.classList.contains("hidden")) {
        dropdown.classList.remove("hidden");
    } else {
        dropdown.classList.add("hidden");
    }
}    