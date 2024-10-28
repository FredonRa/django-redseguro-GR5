class _BotService {
    constructor() {
        this.client = new HttpClient("/api/bot/");
    }

    async start(data) {
        return await this.client.post('conversacion/iniciar/', data);
    }

    async getConversacionesAnteriores() {
        return await this.client.get(`conversacion/anteriores/`);
    }

    // Obtener todas los tipos de gestiones
    async getTipoGestiones() {
        return await this.client.get('tipoGestiones/');
    }

    async selectTipoGestiones(data) {
        return await this.client.post('tipoGestiones/', data);
    }

    // Obtener todas las gestiones
    async getGestiones(tipo_gestion_id) {
        return await this.client.get('gestiones/' + tipo_gestion_id);
    }

    async selectGestion(data) {
        return await this.client.post('gestiones/seleccionar_gestion/', data);
    }

    async getOpciones() {
        return await this.client.get(`opciones/`);
    }

    async selectOpcion(data) {
        return await this.client.post('opciones/seleccionar_opcion/', data);
    }

    async getRespuestas() {
        return await this.client.get(`respuestas/`);
    }

    // Crear un nuevo usuario
    async createUsuario(data) {
        return await this.client.post(``, data);
    }

    // Actualizar un usuario existente
    async updateUsuario(usuarioId, data) {
        return await this.client.put(`${usuarioId}/`, data);
    }

    // Eliminar un usuario
    async deleteUsuario(usuarioId) {
        return await this.client.delete(`${usuarioId}/`);
    }
}