const BotService = new _BotService();

class BotUI {
    constructor() {
        this.conversacionActiva = false;
        this.listarConversacionesAnteriores = false;
        this.containerChat = document.getElementById('container-chat');
        this.containerMensajes = document.getElementById('container-mensajes');
        this.notLoggedIn = document.getElementById('not-logged');
        this.mensajes = document.getElementById('mensajes');
        this.mensajesAnteriores = document.getElementById('mensajes-anteriores');
        this.verConversacionesAnterioresBtn = document.getElementById('ver-conversaciones-anteriores');
        this.backdrop = document.getElementById('backdrop');
        this.opciones = [];
        this.gestiones = [];
        this.conversacionesAnteriores = [];
        this.init();

        // Crear un observer para observar cambios en el contenedor de mensajes
        this.observer = new MutationObserver(() => {
            this.scrollToBottom();
        });

        // Configurar el observer para observar hijos añadidos
        this.observer.observe(this.mensajes, { childList: true });
    }

    async init() {
        try {
            this.setupEventListeners();

            if (this.isLoggedIn()) {
                await this.loadBotData();
                await this.loadPreviousConversations();
                this.startConversation();
                this.containerMensajes.classList.remove("hidden")
                this.notLoggedIn.classList.add("hidden")
            }
        } catch (error) {
            console.error("Error during initialization:", error);
        }
    }

    isLoggedIn() {
        const userInfoCookie = getCookie('session_id');
        return userInfoCookie
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
        this.containerChat.classList[action]('hidden');
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
            await Promise.all(this.conversacionesAnteriores.map(async (conversacion) => this.displayPreviousConversation(conversacion)));
            document.getElementById("fecha-fin-container").classList.remove('hidden');
            this.verConversacionesAnterioresBtn.classList.add("hidden");
            this.disableButtons("mensajes-anteriores");
        } catch (error) {
            console.error("Error showing previous conversations:", error);
        } finally {
            this.listarConversacionesAnteriores = false;
        }
    }

    createFechaInicio(fecha, container) {
        const formattedDate = this.formatDateToISO(fecha);
        const fechaInicioContainer = this.createElement('div', 'w-full py-5 border-t-2 border-gray-200 flex justify-center mt-5');
        const fechaInicio = this.createElement('span', '-mt-10 bg-indigo-300 p-2 px-3 rounded-lg', formattedDate);
        fechaInicioContainer.appendChild(fechaInicio)
        return fechaInicioContainer;
    }

    async displayPreviousConversation(conversacion) {
        const fechaInicio = this.createFechaInicio(conversacion.fecha_inicio);
        const containerConversacion = this.createElement('div');
        this.mensajesAnteriores.appendChild(containerConversacion)
        containerConversacion.appendChild(fechaInicio);
        await this.listConversation(conversacion.gestion, containerConversacion);
    }

    async listConversation(gestion, container = this.mensajes) {
        if (!gestion) return;

        const { conversacion_gestion_id, nombre, pasos } = gestion;
        const containerGestion = this.createElement('div');
        await this.listGestiones(this.gestiones, container);

        this.createUserMessage(containerGestion, nombre, true)
        container.appendChild(containerGestion);

        if (pasos) {
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
            this.createUserMessage(container, nombre)
            if (respuestas) this.listRespuestas(respuestas, container);
        }
    }

    async listGestiones(gestiones, container = this.mensajes) {
        const containerGestiones = this.createElement('div', "flex flex-col gap-2");
        const gestionesDiv = this.createElement('div', "mb-2 w-full gap-2 flex flex-col");

        gestiones.forEach(({ gestion_id, nombre }) => {
            this.createButton(gestionesDiv, gestion_id, nombre, () => this.handleGestionSelection(gestion_id, nombre));
        });

        this.createBotMessage(gestionesDiv, containerGestiones, "Para comenzar, seleccione una gestión:");
        container.appendChild(containerGestiones);
    }

    async handleGestionSelection(gestion_id, nombre) {
        try {
            const { conversacion_gestion_id, opciones } = await BotService.selectGestion({ gestion_id });
            this.createUserMessage(this.mensajes, nombre);
            this.disableButtons(this.mensajes.id);
            await this.listOpciones(opciones, conversacion_gestion_id);
        } catch (error) {
            console.error("Error selecting gestion:", error);
        }
    }

    async listOpciones(opciones, conversacion_gestion_id, container = this.mensajes) {
        const containerOpciones = this.createElement('div', "flex flex-col gap-2");
        const opcionesDiv = this.createElement('div', "mb-2 w-full gap-2 flex flex-col");

        opciones.forEach(({ opcion_id, nombre, paso }) => {
            this.createButton(opcionesDiv, opcion_id, nombre, async () => {
                await this.handleOpcionSelection(opcion_id, conversacion_gestion_id, paso, nombre);
            });
        });

        this.createBotMessage(opcionesDiv, containerOpciones, "Seleccione una opción:");
        container.appendChild(containerOpciones);
    }

    async handleOpcionSelection(opcion_id, conversacion_gestion_id, paso_id, nombre) {
        try {
            const { respuestas, opciones } = await BotService.selectOpcion({ opcion_id, conversacion_gestion_id, paso_id });
            this.createUserMessage(this.mensajes, nombre)
            this.disableButtons(this.mensajes.id);
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
        this.createBotMessage(options, this.mensajes, "¿Desea realizar otra consulta?", false)
    }

    createContinuationOptions() {
        const options = [
            {
                text: "Si",
                onclick: async () => {
                    this.disableButtons(this.mensajes.id)
                    await this.startConversation();
                }
            },
            {
                text: "No",
                onclick: async () => {
                    const containerRespuestas = this.createElement('div', 'flex flex-col gap-2');
                    this.disableButtons(this.mensajes.id)
                    this.createMessage(containerRespuestas, "Muchas gracias por haberte comunicado.", false);
                    this.createMessage(containerRespuestas, "Recorda que ante cualquier consulta estoy aquí para ayudarte.", false);
                    this.createMessage(containerRespuestas, "¡Que tengas lindo día!", false);

                    this.createBotMessage(containerRespuestas, this.mensajes, null, false)
                }
            }
        ];

        const containerOpciones = this.createElement('div', "mb-2 w-full gap-2 flex");

        options.forEach(({ text, onclick }) => {
            this.createButton(containerOpciones, "", text, async () => {
                this.createUserMessage(this.mensajes, text)
                await onclick();
            });
        });

        return containerOpciones;
    }

    async endConversation() {
        this.conversacionActiva = false; // Finaliza la conversación
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
    }

    createBotMessage(content, container, labelText) {
        // Crear el contenedor principal
        const messageContainer = this.createElement('div', 'flex items-start gap-4 mb-4 ');
        // Crear el contenedor para el avatar (parte izquierda)
        const avatarContainer = this.createElement('div', 'flex-shrink-0');
        const avatar = this.createElement('img', 'h-12 w-12 rounded-full', '', '', null);
        avatar.src = botIcon; // Cambia esto por la URL del avatar del bot
        avatar.alt = 'Bot Avatar';
        avatarContainer.appendChild(avatar);

        // Crear el contenedor para el contenido (parte derecha)
        const contentContainer = this.createElement('div', 'flex flex-col w-full pt-2 gap-2');

        if (labelText) this.createMessage(contentContainer, labelText, false)

        // Agregar avatar y contenido al contenedor principal
        messageContainer.appendChild(avatarContainer);
        contentContainer.appendChild(content); // Asignar el contenido que viene por parámetro
        messageContainer.appendChild(contentContainer);

        // Agregar el mensaje al contenedor de mensajes
        if (container) {
            container.appendChild(messageContainer)
        } else {
            this.mensajes.appendChild(messageContainer);
        }
    }

    createUserMessage(container, text) {
        // Crear el contenedor principal
        const messageContainer = this.createElement('div', 'flex items-start gap-4 mb-4 ');

        // Crear el contenedor para el avatar (parte izquierda)
        const avatarContainer = this.createElement('div', 'flex-shrink-0');
        const avatar = this.createElement('img', 'h-12 w-12 rounded-full', '', '', null);
        avatar.src = femaleIcon; // Cambia esto por la URL del avatar del bot
        avatar.alt = 'Female Avatar';
        avatarContainer.appendChild(avatar);

        // Crear el contenedor para el contenido (parte derecha)
        const contentContainer = this.createElement('div', 'w-full pt-2');

        this.createMessage(contentContainer, text, true)
        // Agregar avatar y contenido al contenedor principal
        messageContainer.appendChild(contentContainer);
        messageContainer.appendChild(avatarContainer);

        // Agregar el mensaje al contenedor de mensajes
        if (container) {
            container.appendChild(messageContainer)
        } else {
            this.mensajes.appendChild(messageContainer);
        }
    }

    scrollToBottom() {
        this.containerMensajes.scrollTop = this.mensajes.scrollHeight;
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
