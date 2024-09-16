
document.addEventListener("DOMContentLoaded", async () => {
    // Obtener la entidad de la URL
    const entity = getEntityFromPath();

    const CrudService = new _CrudService(entity);

    if (!entity) {
        alert("Entidad no especificada en la URL.");
        return;
    }

    // Asignar el título de la entidad
    document.getElementById("crud-title").textContent = `Gestionar ${entity}`;

    // Función para obtener los campos y datos de la entidad de la API
    CrudService.getFields()
        .then(data => {
            console.log("data", data)
            buildForm(data)
        })
        .catch(error => console.error("Error al obtener los campos:", error));

    CrudService.getAll()
        .then(data => buildTable(data))
        .catch(error => console.error("Error al obtener los datos:", error));

    // Generar formulario dinámico
    function buildForm(fields) {
        console.log("fields", fields)
        const formFieldsContainer = document.getElementById("form-fields");
        formFieldsContainer.innerHTML = '';

        fields.forEach(field => {
            const input = document.createElement('input');
            input.type = field.type;
            input.name = field.name;
            input.placeholder = formatFieldName(field.name);
            input.className = 'border px-4 py-2 w-full mt-2 rounded-md';

            formFieldsContainer.appendChild(input);
        });

        const form = document.getElementById("entityForm");
        form.onsubmit = handleFormSubmit;
    }

    // Manejador del submit del formulario
    function handleFormSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);

        const entityData = {};
        formData.forEach((value, key) => {
            entityData[key] = value;
        });

        fetch(`/api/${entity}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(entityData),
        })
            .then(response => response.json())
            .then(data => {
                alert(`${entity} guardado correctamente!`);
                fetch(`/api/${entity}`)
                    .then(response => response.json())
                    .then(data => buildTable(data))
                    .catch(error => console.error("Error al obtener los datos:", error));
            })
            .catch(error => console.error("Error al guardar:", error));
    }

    // Generar tabla dinámica
    function buildTable(data) {
        const tableHeaders = document.getElementById("table-headers");
        const tableBody = document.getElementById("table-body");

        tableHeaders.innerHTML = '';
        tableBody.innerHTML = '';

        if (data.length === 0) return;

        // Crear encabezados de tabla
        const headers = Object.keys(data[0]);
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            th.className = 'px-4 py-2';
            tableHeaders.appendChild(th);
        });

        // Crear filas de la tabla
        data.forEach(item => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = item[header];
                td.className = 'border px-4 py-2';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
});

function getEntityFromPath() {
    const pathSegments = window.location.pathname.split('/').filter(item => item !== "");
    // Assuming the entity is the last segment in the path
    const entity = pathSegments[pathSegments.length - 1];
    return entity;
}

function formatFieldName(fieldName) {
    return fieldName
        .replace(/_/g, ' ')  // Reemplaza guiones bajos con espacios
        .replace(/\b\w/g, char => char.toUpperCase());  // Capitaliza la primera letra de cada palabra
}