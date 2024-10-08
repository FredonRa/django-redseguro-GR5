const API_BASE_URL = '/auth/';

class _AuthService {
    constructor() {
        this.client = new HttpClient(API_BASE_URL);
    }

    async auth(data) {
        return await this.client.post(``, data);
    }
}