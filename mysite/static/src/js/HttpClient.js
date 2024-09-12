class HttpClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    // Método genérico para manejar las peticiones HTTP
    async request(endpoint, method = 'GET', data = null, headers = {}) {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('HTTP Request Error:', error);
            throw error;
        }
    }

    // Petición GET
    get(endpoint, headers = {}) {
        return this.request(endpoint, 'GET', null, headers);
    }

    // Petición POST
    post(endpoint, data, headers = {}) {
        return this.request(endpoint, 'POST', data, headers);
    }

    // Petición PUT
    put(endpoint, data, headers = {}) {
        return this.request(endpoint, 'PUT', data, headers);
    }

    // Petición DELETE
    delete(endpoint, headers = {}) {
        return this.request(endpoint, 'DELETE', null, headers);
    }
}