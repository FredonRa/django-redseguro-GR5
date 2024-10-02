const API_BASE_URL = '/api/login/';

class _AuthService {
    constructor() {
        this.client = new HttpClient(API_BASE_URL);
    }

    async authUsuario(data) {
        return await this.client.post(``, data);
    }
}