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
    async updatePassword(nueva_contrasenia) {
        try {
            const response = await this.client.post('update-password/', {
                nueva_contrasenia: nueva_contrasenia
            });
            console.log('Contraseña actualizada correctamente:', response.data);
            return response.data;
        } catch (error) {
            console.error('Error al actualizar la contraseña:', error);
            throw error;  // Lanza el error para ser capturado donde se llame a esta función
        }
    }

    // Eliminar un usuario
    async deleteUsuario(usuarioId) {
        return await this.client.delete(`${usuarioId}/`);
    }
}