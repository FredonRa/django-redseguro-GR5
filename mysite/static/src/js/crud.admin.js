document.addEventListener("DOMContentLoaded", async () => {
    const entityName = getEntityFromPath();

    if (!entityName) {
        alert("Entidad no especificada en la URL.");
        return;
    }

    const CrudService = new _CrudService(entityName);
    document.getElementById("crud-title").textContent = `${entityName}`;

    // Configuración de formularios y tabla
    try {
        const [data, fields, actions] = await Promise.all([
            CrudService.getAll(),
            CrudService.getFields(),
            CrudService.getActions(),
        ]);

        buildTable(data, fields);
        if (fields) buildForm(fields);
        if (actions) handleActions(actions, CrudService, fields);
    } catch (error) {
        console.error(error)
        // handleError(error);
    }

    // Función para construir el formulario
    function buildForm(fields) {
        const formCreate = document.getElementById("modal-create-entity-form");
        const formUpdate = document.getElementById("modal-update-entity-form");
        const formCreateFieldsContainer = document.getElementById("modal-create-form-fields");
        const formUpdateFieldsContainer = document.getElementById("modal-update-form-fields");

        formCreateFieldsContainer.innerHTML = '';
        formUpdateFieldsContainer.innerHTML = '';

        fields.forEach(field => {
            const formGroup = createFormGroup(field);
            if (field.editable) formCreateFieldsContainer.appendChild(formGroup.cloneNode(true));
            formUpdateFieldsContainer.appendChild(formGroup);
        });

        formCreate.onsubmit = handleFormCreateSubmit;
        formUpdate.onsubmit = handleFormUpdateSubmit;
    }

    // Función para crear el grupo de formulario (label + input/select)
    function createFormGroup(field) {
        const formGroup = document.createElement('div');
        formGroup.className = 'mb-4';

        const label = createLabel(field.name);
        const inputOrSelect = createInput(field);

        formGroup.appendChild(label);
        formGroup.appendChild(inputOrSelect);

        return formGroup;
    }

    function createLabel(fieldName) {
        const label = document.createElement('label');
        label.textContent = formatFieldName(fieldName);
        label.htmlFor = fieldName;
        label.className = 'block text-gray-700 font-bold mb-2';
        return label;
    }

    function createInput(field) {
        const input = field.type === 'select' ? document.createElement('select') : document.createElement('input');
        const isEditableInput = field.editable;
        input.name = field.name;
        input.id = field.name;
        input.className = 'border px-4 py-2 w-full mt-2 rounded-md disabled:pointer-events-none disabled:bg-gray-200';
        input.disabled = !isEditableInput;

        if (field.type !== 'select') {
            input.type = field.type;
            input.placeholder = formatFieldName(field.name);
        }
        return input;
    }

    // Función para manejar el envío de formularios
    async function handleFormCreateSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const entityData = Object.fromEntries(formData.entries());

        try {
            await CrudService.create(entityData);
            alert(`${entityName} guardado correctamente!`);
            const updatedData = await CrudService.getAll();
            buildTable(updatedData);
        } catch (error) {
            handleError(error);
        }
    }

    async function handleFormUpdateSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const entityData = Object.fromEntries(formData.entries());

        try {
            await CrudService.put(entityData);
            alert(`${entityName} guardado correctamente!`);
            const updatedData = await CrudService.getAll();
            buildTable(updatedData);
        } catch (error) {
            handleError(error);
        }
    }

    // Función para construir la tabla
    function buildTable(data, fields) {
        const tableFields = document.getElementById("table-headers");
        const tableBody = document.getElementById("table-body");
        const thActions = document.createElement('th');

        tableFields.innerHTML = '';
        tableBody.innerHTML = '';

        fields.forEach(field => {
            const th = document.createElement('th');
            th.textContent = formatFieldName(field.name);
            th.className = 'px-4 py-2';
            tableFields.appendChild(th);
        });

        tableFields.appendChild(thActions);

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.id = "tr-" + item[getEntityIdName(entityName)];
            const tdActions = document.createElement('td');

            fields.forEach(field => {
                const td = document.createElement('td');
                td.textContent = item[field.name] ?? "-";
                td.className = 'border px-4 py-2 text-center';
                tr.appendChild(td);
            });

            const actionsCell = createActionsCell(item[getEntityIdName(entityName)]);
            tdActions.appendChild(actionsCell);
            tr.appendChild(tdActions);
            tableBody.appendChild(tr);
        });
    }

    // Función para crear la td de acciones
    function createActionsCell(entityId) {
        const tdActions = document.createElement('td');
        const updateBtn = document.createElement("button");

        updateBtn.className = "open-update-modal p-2";
        updateBtn.dataset.id = entityId;
        updateBtn.type = "button";

        const svg = createEditIcon();
        updateBtn.appendChild(svg);

        tdActions.appendChild(updateBtn);
        return tdActions;
    }

    function createEditIcon() {
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");

        svg.setAttribute("class", "feather feather-edit");
        svg.setAttribute("fill", "none");
        svg.setAttribute("height", "24");
        svg.setAttribute("stroke", "currentColor");
        svg.setAttribute("stroke-linecap", "round");
        svg.setAttribute("stroke-linejoin", "round");
        svg.setAttribute("stroke-width", "2");
        svg.setAttribute("viewBox", "0 0 24 24");
        svg.setAttribute("width", "24");

        const path1 = document.createElementNS(svgNS, "path");
        path1.setAttribute("d", "M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7");
        const path2 = document.createElementNS(svgNS, "path");
        path2.setAttribute("d", "M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z");

        svg.appendChild(path1);
        svg.appendChild(path2);
        return svg;
    }

    // Función para manejar las acciones de create/edit/delete(para futuro)
    function handleActions(actions, service, fields) {
        const { crear, editar } = actions;

        if (crear) setupModal("modal-create", "open-create-modal", service);
        if (editar) setupUpdateModal("modal-update", "open-update-modal", service, fields);
    }

    function setupModal(modalId, triggerId) {
        const modal = document.getElementById(modalId);
        const openModalBtn = document.getElementById(triggerId);
        const closeModalBtn = modal.querySelector('#close-create-modal');

        openModalBtn.addEventListener('click', () => toggleModal(modal, true));
        closeModalBtn.addEventListener('click', () => toggleModal(modal, false));

        modal.addEventListener('click', (event) => {
            if (event.target === modal) toggleModal(modal, false);
        });
    }

    function setupUpdateModal(modalId, triggerClass, service, fields) {
        const modal = document.getElementById(modalId);
        const openModalBtns = document.querySelectorAll(`.${triggerClass}`);
        const closeModalBtn = modal.querySelector('#close-update-modal');

        openModalBtns.forEach(btn => {
            btn.addEventListener('click', async () => {
                const entityId = btn.dataset.id;
                try {
                    const entityData = await service.getById(entityId);
                    fillUpdateForm(entityData, fields);
                    toggleModal(modal, true);
                } catch (error) {
                    handleError(error);
                }
            });
        });

        closeModalBtn.addEventListener('click', () => toggleModal(modal, false));

        modal.addEventListener('click', (event) => {
            if (event.target === modal) toggleModal(modal, false);
        });
    }

    // Función para abrir/cerrar modales
    function toggleModal(modal, show) {
        const modalContent = modal.querySelector('.bg-white');
        if (show) {
            modal.classList.remove('pointer-events-none', 'opacity-0');
            modal.classList.add('opacity-100');
            modalContent.classList.add('scale-100');
        } else {
            modal.classList.add('opacity-0');
            modal.classList.remove('opacity-100');
            modalContent.classList.remove('scale-100');
            setTimeout(() => modal.classList.add('pointer-events-none'), 300);
        }
    }

    // Funciones auxiliares
    function formatFieldName(name) {
        return name.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
    }

    function getEntityIdName(entity) {
        const entities = {
            usuarios: "usuario_id",
            conversaciones: "conversacion_id",
            gestiones: "gestion_id",
            pasos: "paso_id",
            opciones: "opcion_id",
            respuestas: "respuesta_id"
        }
        return entities[entityName];
    }

    function getEntityFromPath() {
        const pathParts = window.location.pathname.split('/');
        return pathParts[2] || null;
    }

    function handleError(error) {
        console.error("Error:", error);
        alert("Ha ocurrido un error, por favor intenta de nuevo.");
    }

    async function fillUpdateForm(data, fields) {
        const updateForm = document.getElementById('modal-update-entity-form');
        const modelsApi = {
            usuario: "usuarios",
            conversacion: "conversaciones",
            gestion: "gestiones",
            paso: "pasos",
            opcion: "opciones",
            respuesta: "respuestas"
        };

        for (const key of Object.keys(data)) {
            const input = updateForm.querySelector(`[name="${key}"]`);
            if (!input || !data[key]) continue;

            if (input.type === "select-one") {
                await populateSelectOptions(input, key, modelsApi[key], fields);
            } else {
                input.value = input.type === "datetime-local" ? formatDateToISO(data[key]) : data[key];
            }
        }
    }

    async function populateSelectOptions(input, key, model, fields) {
        const CrudService = new _CrudService(model);

        try {
            const data = await CrudService.getAll();
            const entityOptions = fields.find(field => field.name === key)?.options || [];

            data.forEach(entity => {
                const [entityIdField, ...entityValueFields] = entityOptions;
                const entityId = entity[entityIdField];
                const entityValues = entityValueFields.map(field => entity[field]);

                const option = document.createElement('option');
                option.value = entityId;
                option.text = `#${entityId} - ${concatenateStrings(entityValues)}`;
                input.appendChild(option);
            });
        } catch (err) {
            console.error("Error al obtener las entidades para el select:", err);
        }
    }

    function formatDateToISO(dateStr) {
        if (typeof moment === 'undefined') {
            console.error('Moment.js no está disponible');
            return null;
        }

        // Convierte la fecha al formato deseado
        return moment(dateStr).format('YYYY-MM-DDTHH:mm');
    }

    function concatenateStrings(strings) {
        return strings.join(' ');
    }
});
