const BotService = new _BotService();

class BotUI {
    constructor() {
        this.conversacionActiva = false;
        this.listarConversacionesAnteriores = false;
        this.chatContainer = document.getElementById('chatContainer');
        this.mensajes = document.getElementById('mensajes');
        this.mensajesAnteriores = document.getElementById('mensajes-anteriores');
        this.verConversacionesAnterioresBtn = document.getElementById('ver-conversaciones-anteriores');
        this.backdrop = document.getElementById('backdrop');
        this.opciones = [];
        this.gestiones = [];
        this.conversacionesAnteriores = [];
        this.init();
    }

    async init() {
        try {
            await this.loadBotData();
            this.setupEventListeners();
            await this.loadPreviousConversations();
            this.startConversation();
        } catch (error) {
            console.error("Error during initialization:", error);
        }
    }

    async loadBotData() {
        const [opcionesData, gestionesData] = await Promise.all([
            BotService.getOpciones(),
            BotService.getGestiones()
        ]);
        this.opciones = opcionesData.opciones;
        this.gestiones = gestionesData.gestiones;
    }

    setupEventListeners() {
        document.getElementById('chatButton').addEventListener('click', () => this.toggleChat(true));
        this.backdrop.addEventListener('click', () => this.toggleChat(false));
        this.verConversacionesAnterioresBtn.addEventListener('click', () => this.showPreviousConversations());
    }

    toggleChat(isVisible) {
        const action = isVisible ? 'remove' : 'add';
        this.chatContainer.classList[action]('hidden');
        this.backdrop.classList[action]('hidden');
    }

    async startConversation() {
        try {
            this.conversacionActiva = true;
            const { gestion } = await BotService.start({ usuario: 14 });
            gestion ? this.listConversation(gestion) : this.listGestiones(this.gestiones);
        } catch (error) {
            console.error("Error starting conversation:", error);
        }
    }

    async loadPreviousConversations() {
        try {
            const conversacionesAnteriores = await BotService.getConversacionesAnteriores(14);
            if (conversacionesAnteriores.length) {
                this.verConversacionesAnterioresBtn.classList.remove("hidden");
                this.conversacionesAnteriores = conversacionesAnteriores;
            }
        } catch (error) {
            console.error("Error loading previous conversations:", error);
        }
    }

    async showPreviousConversations() {
        try {
            this.listarConversacionesAnteriores = true;
            await Promise.all(this.conversacionesAnteriores.map(conversacion => this.displayPreviousConversation(conversacion)));
            document.getElementById("fecha-fin-container").classList.remove('hidden');
            this.verConversacionesAnterioresBtn.classList.add("hidden");
            this.disableButtons("mensajes-anteriores");
        } catch (error) {
            console.error("Error showing previous conversations:", error);
        } finally {
            this.listarConversacionesAnteriores = false;
        }
    }

    createFechaInicio(fecha) {
        const formattedDate = this.formatDateToISO(fecha);
        const fechaInicioContainer = this.createElement('div', 'w-full py-5 border-t-2 border-gray-200 flex justify-center mt-5');
        const fechaInicio = this.createElement('span', '-mt-10 bg-indigo-300 p-2 px-3 rounded-lg', formattedDate);
        fechaInicioContainer.appendChild(fechaInicio)
        return fechaInicioContainer;
    }

    async displayPreviousConversation(conversacion) {
        const fechaInicio = this.createFechaInicio(conversacion.fecha_inicio);
        this.mensajesAnteriores.appendChild(fechaInicio);
        await this.listConversation(conversacion.gestion, this.mensajesAnteriores);
    }

    async listConversation(gestion, container = this.mensajes) {
        if (!gestion) return;

        const { conversacion_gestion_id, nombre, pasos } = gestion;
        const containerGestion = this.createElement('div');
        this.listGestiones(this.gestiones, container);
        this.createMessage(containerGestion, nombre, true);
        container.appendChild(containerGestion);

        if (pasos) {
            this.disableButtons(container.id);
            for (const paso of pasos) {
                await this.handlePaso(paso, conversacion_gestion_id, container);
            }
        }
    }

    async handlePaso(paso, conversacion_gestion_id, container) {
        const { paso: paso_id, opcion } = paso;
        const opcionesFiltradas = this.opciones.filter(opcion => opcion.paso === paso_id);
        await this.listOpciones(opcionesFiltradas, conversacion_gestion_id, container);

        if (opcion) {
            const { nombre, respuestas } = opcion;
            this.createMessage(container, nombre, true);
            if (respuestas) this.listRespuestas(respuestas, this.mensajesAnteriores);
        }
    }

    async listGestiones(gestiones, container = this.mensajes) {
        const containerGestiones = this.createElement('div', "flex flex-col gap-2");
        const gestionesDiv = this.createElement('div', "mb-2 w-full gap-2 flex flex-col");

        this.createMessage(containerGestiones, "Para comenzar, seleccione una gestión:", false);

        gestiones.forEach(({ gestion_id, nombre }) => {
            this.createButton(gestionesDiv, gestion_id, nombre, () => this.handleGestionSelection(gestion_id, nombre));
        });

        containerGestiones.appendChild(gestionesDiv);
        this.createBotMessage(containerGestiones, container)
    }

    async handleGestionSelection(gestion_id, nombre) {
        try {
            const { conversacion_gestion_id, opciones } = await BotService.selectGestion({ gestion_id });
            this.createMessage(this.mensajes, nombre, true);
            await this.listOpciones(opciones, conversacion_gestion_id);
        } catch (error) {
            console.error("Error selecting gestion:", error);
        }
    }

    async listOpciones(opciones, conversacion_gestion_id, container = this.mensajes) {
        const containerOpciones = this.createElement('div', "flex flex-col gap-2");
        const opcionesDiv = this.createElement('div', "mb-2 w-full gap-2 flex flex-col");
        const textoOpciones = this.createElement('span', "", "");

        this.createMessage(containerOpciones, "Seleccione una opción:", false);

        opciones.forEach(({ opcion_id, nombre, paso }) => {
            this.createButton(opcionesDiv, opcion_id, nombre, async () => {
                await this.handleOpcionSelection(opcion_id, conversacion_gestion_id, paso, nombre);
            });
        });

        containerOpciones.appendChild(opcionesDiv);
        this.createBotMessage(containerOpciones, container)
    }

    async handleOpcionSelection(opcion_id, conversacion_gestion_id, paso_id, nombre) {
        try {
            const { respuestas, opciones } = await BotService.selectOpcion({ opcion_id, conversacion_gestion_id, paso_id });
            this.createMessage(this.mensajes, nombre, true);
            if (opciones) await this.listOpciones(opciones, conversacion_gestion_id);
            if (respuestas) this.listRespuestas(respuestas);
        } catch (error) {
            console.error("Error selecting opcion:", error);
        }
    }

    listRespuestas(respuestas, container = this.mensajes) {
        const containerRespuestas = this.createElement('div', 'flex flex-col gap-2');

        respuestas.forEach(({ contenido }) => {
            const respuesta = this.createElement('div');
            this.createMessage(respuesta, contenido, false);
            containerRespuestas.appendChild(respuesta)
        });

        this.createBotMessage(containerRespuestas, container)

        if (this.conversacionActiva && !this.listarConversacionesAnteriores) {
            this.continueConversation();
        }
    }

    continueConversation() {
        if (!this.conversacionActiva) return;
        const container = this.createElement('div', "flex flex-col gap-2");
        const options = this.createContinuationOptions();
        this.createMessage(container, "¿Desea realizar otra consulta?", false);
        container.appendChild(options)
        this.createBotMessage(container)
    }

    createContinuationOptions() {
        const options = [
            {
                text: "Si",
                onclick: async () => {
                    await this.startConversation();
                }
            },
            {
                text: "No",
                onclick: async () => {
                    const containerRespuestas = this.createElement('div', 'flex flex-col gap-2');

                    this.createMessage(containerRespuestas, "Muchas gracias por haberte comunicado.", false);
                    this.createMessage(containerRespuestas, "Recorda que ante cualquier consulta estoy aquí para ayudarte.", false);
                    this.createMessage(containerRespuestas, "¡Que tengas lindo día!", false);

                    this.createBotMessage(containerRespuestas)
                }
            }
        ];

        const containerOpciones = this.createElement('div', "mb-2 w-full gap-2 flex");

        options.forEach(({ text, onclick }) => {
            this.createButton(containerOpciones, "", text, async () => {
                const containerMessage = this.createElement('div');
                this.createMessage(containerMessage, text, true);
                this.mensajes.appendChild(containerMessage);
                await onclick();
            });
        });

        return containerOpciones;
    }

    async endConversation() {
        this.conversacionActiva = false; // Finaliza la conversación
        // Aquí puedes añadir cualquier otra lógica necesaria al final de la conversación
    }

    createElement(tag, classes = '', text = '', id = '', onclick = null) {
        const element = document.createElement(tag);
        if (classes) element.className = classes;
        if (text) element.innerText = text;
        if (id) element.id = id;
        if (onclick) element.onclick = onclick;
        return element;
    }

    createButton(container, id, text, onclick) {
        const button = this.createElement('button', "bg-indigo-600 p-2 rounded-lg w-fit self-center text-white", text, id);
        button.onclick = onclick;
        container.appendChild(button);
    }

    createMessage(container, text, isUser) {
        const containerMessage = this.createElement('div', `flex ${isUser ? 'justify-end' : ''}`);
        const message = this.createElement('div', `p-2 flex rounded-lg w-fit ${isUser ? 'self-end bg-indigo-500 text-white' : 'bg-gray-200'}`, text);
        containerMessage.appendChild(message);
        container.appendChild(containerMessage);
        this.scrollToBottom();
    }

    createBotMessage(content, container) {
        // Crear el contenedor principal
        const messageContainer = this.createElement('div', 'flex items-start gap-4 mb-4 ');

        // Crear el contenedor para el avatar (parte izquierda)
        const avatarContainer = this.createElement('div', 'flex-shrink-0');
        const avatar = this.createElement('img', 'h-12 w-12 rounded-full', '', '', null);
        avatar.src = botIcon; // Cambia esto por la URL del avatar del bot
        avatar.alt = 'Bot Avatar';
        avatarContainer.appendChild(avatar);

        // Crear el contenedor para el contenido (parte derecha)
        const contentContainer = this.createElement('div', 'w-full pt-2');
        contentContainer.appendChild(content); // Asignar el contenido que viene por parámetro

        // Agregar avatar y contenido al contenedor principal
        messageContainer.appendChild(avatarContainer);
        messageContainer.appendChild(contentContainer);

        // Agregar el mensaje al contenedor de mensajes
        if (container) {
            container.appendChild(messageContainer)
        } else {
            this.mensajes.appendChild(messageContainer);
        }
        // Desplazarse hacia abajo automáticamente
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.mensajes.scrollTop = this.mensajes.scrollHeight;
    }

    disableButtons(containerId) {
        const container = document.getElementById(containerId);
        const buttons = container.querySelectorAll('button');
        buttons.forEach(button => button.disabled = true);
    }

    formatDateToISO(dateStr) {
        return moment(dateStr).format('YYYY-MM-DD HH:mm');
    }
}

document.addEventListener("DOMContentLoaded", () => new BotUI());
