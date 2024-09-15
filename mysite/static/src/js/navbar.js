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