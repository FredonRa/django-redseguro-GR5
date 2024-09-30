const BotService = new _BotService();

class BotUI {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.mensajes = document.getElementById('mensajes');
        this.mensajesAnteriores = document.getElementById('mensajes-anteriores');
        this.verConversacionesAnterioresBtn = document.getElementById('ver-conversaciones-anteriores');
        this.backdrop = document.getElementById('backdrop');
        this.opciones = [];
        this.gestiones = [];
        this.init();
    }

    async init() {
        try {
            await this.loadBotData();
            this.setupEventListeners();
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
        document.getElementById('chatButton').addEventListener('click', () => this.showChat());
        this.backdrop.addEventListener('click', () => this.hideChat());
        this.verConversacionesAnterioresBtn.addEventListener('click', () => this.showPreviousConversations());
    }

    showChat() {
        this.chatContainer.classList.remove('hidden');
        this.backdrop.classList.remove('hidden');
    }

    hideChat() {
        this.chatContainer.classList.add('hidden');
        this.backdrop.classList.add('hidden');
    }

    async startConversation() {
        try {
            const { gestion } = await BotService.start({ usuario: 14 });
            await this.loadPreviousConversations();
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
            for (const conversacion of this.conversacionesAnteriores) {
                const fechaInicio = this.createFechaInicio(conversacion.fecha_inicio);
                this.mensajesAnteriores.appendChild(fechaInicio);
                await this.listConversation(conversacion.gestion, this.mensajesAnteriores);
            }
            document.getElementById("fecha-fin-container").classList.remove('hidden');
            this.verConversacionesAnterioresBtn.classList.add("hidden");
            this.disableButtons("mensajes-anteriores");
        } catch (error) {
            console.error("Error showing previous conversations:", error);
        }
    }

    async listConversation(gestion, container = this.mensajes) {
        try {
            if (gestion) {
                const { conversacion_gestion_id, nombre, pasos } = gestion;
                const containerGestion = this.createElement('div');
                this.listGestiones(this.gestiones, container)
                this.createMessage(containerGestion, nombre, true);
                container.appendChild(containerGestion);
                if (pasos) {
                    this.disableButtons(container.id);
                    for (const paso of pasos) {
                        const { paso: paso_id, opcion } = paso;
                        const opcionesFiltradas = this.opciones.filter(opcion => opcion.paso === paso_id);
                        await this.listOpciones(opcionesFiltradas, conversacion_gestion_id, container);
                        if (opcion) {
                            const { nombre, respuestas } = opcion
                            const containerPaso = this.createElement('div');
                            this.createMessage(containerPaso, nombre, true);
                            container.appendChild(containerPaso);
                            if (respuestas) this.listRespuestas(respuestas, this.mensajesAnteriores);
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Error listing conversation:", error);
        }
    }

    async listGestiones(gestiones, container = this.mensajes) {
        const containerGestiones = this.createElement('div', "mb-2 w-full gap-2 flex");
        gestiones.forEach(({ gestion_id, nombre }) => {
            this.createButton(containerGestiones, gestion_id, nombre, () => this.handleGestionSelection(gestion_id, nombre));
        });
        container.appendChild(containerGestiones);
    }

    async handleGestionSelection(gestion_id, nombre) {
        try {
            const { conversacion_gestion_id, opciones } = await BotService.selectGestion({ gestion_id });
            const containerRespuesta = this.createElement('div');
            this.createMessage(containerRespuesta, nombre, true);
            this.mensajes.appendChild(containerRespuesta)
            this.listOpciones(opciones, conversacion_gestion_id);
        } catch (error) {
            console.error("Error selecting gestion:", error);
        }
    }

    async listOpciones(opciones, conversacion_gestion_id, container = this.mensajes) {
        const containerOpciones = this.createElement('div', "mb-2 w-full gap-2 flex");
        opciones.forEach(({ opcion_id, nombre, paso }) => {
            this.createButton(containerOpciones, opcion_id, nombre, async () => {
                await this.handleOpcionSelection(opcion_id, conversacion_gestion_id, paso, nombre);
            });
        });
        container.appendChild(containerOpciones);
    }

    async handleOpcionSelection(opcion_id, conversacion_gestion_id, paso_id, nombre) {
        try {
            const { respuestas, opciones } = await BotService.selectOpcion({ opcion_id, conversacion_gestion_id, paso_id });
            const containerRespuesta = this.createElement('div');
            this.createMessage(containerRespuesta, nombre, true);
            this.mensajes.appendChild(containerRespuesta)
            if (opciones) this.listOpciones(opciones, conversacion_gestion_id);
            if (respuestas) this.listRespuestas(respuestas);
        } catch (error) {
            console.error("Error selecting opcion:", error);
        }
    }

    listRespuestas(respuestas, container = this.mensajes) {
        respuestas.forEach(({ contenido }) => {
            const containerRespuesta = this.createElement('div', "mb-2 w-1/2 gap-2 flex");
            this.createMessage(containerRespuesta, contenido, false);
            container.appendChild(containerRespuesta);
        });
        this.scrollToBottom();
    }

    createElement(tag, classes = '', text = '', id = '', onclick = null) {
        const element = document.createElement(tag);
        if (classes) element.className = classes;
        if (text) element.textContent = text;
        if (id) element.id = id;
        if (onclick) element.onclick = onclick;
        return element;
    }

    createButton(container, id, text, onclick) {
        const button = this.createElement('button', "bg-gray-200 p-2 rounded-lg w-fit", text, id);
        button.onclick = () => {
            this.disableButtons("chatContainer");
            onclick();
        };
        container.appendChild(button);
    }

    createMessage(container, text, isUser = true) {
        const messageClass = isUser
            ? "bg-indigo-500 text-white p-2 rounded-lg self-end w-fit"
            : "bg-gray-200 p-2 rounded-lg w-fit";
        const messageDiv = this.createElement('div', messageClass, text);
        container.className = isUser ? "mb-2 w-full gap-2 flex justify-end" : "mb-2 w-full gap-2 flex";
        container.appendChild(messageDiv);
    }

    disableButtons(containerId) {
        const buttons = document.querySelectorAll(`#${containerId} button`);
        buttons.forEach(button => (button.onclick = null));
    }

    createFechaInicio(fecha) {
        const formattedDate = this.formatDateToISO(fecha);
        const fechaInicioContainer = this.createElement('div', 'w-full py-5 border-t-2 border-gray-200 flex justify-center mt-5');
        const fechaInicio = this.createElement('span', '-mt-10 bg-indigo-300 p-2 px-3 rounded-lg', formattedDate);
        fechaInicioContainer.appendChild(fechaInicio)
        return fechaInicioContainer;
    }

    scrollToBottom() {
        this.mensajes.scrollTop = this.mensajes.scrollHeight;
    }

    formatDateToISO(dateStr) {
        return moment(dateStr).format('YYYY-MM-DD HH:mm');
    }
}

// Inicializar la aplicación del bot
document.addEventListener('DOMContentLoaded', () => {
    new BotUI();
});
