const API_BASE_URL = '/api/usuarios/';

class _UsuarioService {
    constructor() {
        this.client = new HttpClient(API_BASE_URL);
    }

    // Obtener todos los usuarios
    async getUsuarios() {
        return await this.client.get('');
    }

    // Crear un nuevo usuario
    async createUsuario(data) {
        return await this.client.post(``, data);
    }

    // Actualizar un usuario existente
    async updateUsuario(usuarioId, data) {
        return await this.client.put(`${usuarioId}/`, data);
    }

    // Actualizar un contraseña
    async updatePassword(data) {
        return await this.client.post(``, data);
    }

    // Eliminar un usuario
    async deleteUsuario(usuarioId) {
        return await this.client.delete(`${usuarioId}/`);
    }
}