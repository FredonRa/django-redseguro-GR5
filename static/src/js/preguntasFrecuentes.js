const UsuarioService = new _PreguntasFrecuentesService();


window.addEventListener('DOMContentLoaded', function () {
    async function fetchFAQs() {
        try {
            // Llamada a la API para obtener las preguntas frecuentes
            const faqs = await UsuarioService.get();

            const accordionContainer = document.getElementById('accordion');
            accordionContainer.innerHTML = ''; // Limpiamos el contenido previo

            faqs.forEach(faq => {
                // Creamos el contenedor principal para cada pregunta
                const faqItem = document.createElement('div');
                faqItem.className = 'border border-gray-300 border-b-2 border-gray-200';

                // Botón para la pregunta (título)
                const button = document.createElement('button');
                button.className = 'w-full flex gap-2 items-center py-4 text-left text-gray-700 font-medium';
                button.onclick = () => toggleContent(button);

                // Título de la pregunta
                const title = document.createElement('span');
                title.textContent = faq.titulo;

                // Icono de flecha
                const icon = document.createElement('img');
                icon.src = '/static/src/img/chevron_down.png'; // Ruta de tu imagen de flecha
                icon.className = 'w-4 h-4 text-gray-500 transition-transform duration-300';

                // Contenido de la pregunta (respuesta)
                const content = document.createElement('div');
                content.className = 'hidden px-4 pb-4 text-gray-600';
                content.textContent = faq.contenido;

                // Estructura del acordeón
                button.appendChild(icon);
                button.appendChild(title);
                faqItem.appendChild(button);
                faqItem.appendChild(content);
                accordionContainer.appendChild(faqItem);
            });
        } catch (error) {
            console.error('Error al obtener las preguntas frecuentes:', error);
        }
    }

    function toggleContent(button) {
        const content = button.nextElementSibling;
        const icon = button.querySelector('img');

        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            icon.classList.add('rotate-180');
        } else {
            content.classList.add('hidden');
            icon.classList.remove('rotate-180');
        }
    }

    // Llamamos a la función para cargar las preguntas frecuentes
    fetchFAQs();
})

function toggleContent(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('svg');

    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        icon.classList.add('rotate-180');
    } else {
        content.classList.add('hidden');
        icon.classList.remove('rotate-180');
    }
}