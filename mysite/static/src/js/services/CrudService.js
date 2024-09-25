class _CrudService {
    constructor(entity) {
        this.entity = entity;
        this.client = new HttpClient(`/api/${this.entity}/`);
    }

    // Obtener todas las entidades
    async getAll() {
        return await this.client.get('');
    }

    async getById(entityId) {
        return await this.client.get(`${entityId}/`);
    }

    async getFields() {
        return await this.client.get('campos/');
    }

    async getActions() {
        return await this.client.get('acciones/');
    }

    // Crear un nuevo entidad
    async create(data) {
        return await this.client.post(``, data);
    }

    // Actualizar una entidad existente
    async update(entityId, data) {
        return await this.client.put(`${entityId}/`, data);
    }

    // Eliminar un entidad
    async delete(entityId) {
        return await this.client.delete(`${entityId}/`);
    }
}