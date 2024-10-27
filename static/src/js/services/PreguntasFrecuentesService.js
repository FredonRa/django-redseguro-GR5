const API_BASE_URL = '/api/preguntasFrecuentes/';

class _PreguntasFrecuentesService {
    constructor() {
        this.client = new HttpClient(API_BASE_URL);
    }

    async get() {
        return await this.client.get('');
    }
}