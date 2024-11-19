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
    async updateUsuario(data) {
        return await this.client.patch(`actualizar/`, data);
    }

    // Actualizar un contraseña
    async updatePassword(data) {
        return await this.client.patch('cambiar-contrasenia/', data);
    }

    // Eliminar un usuario
    async deleteUsuario(usuarioId) {
        return await this.client.delete(`${usuarioId}/`);
    }
}