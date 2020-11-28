export default class ApiHandler {
    constructor() {
        this._base = 'http://0.0.0.0:8000';
        window.ApiHandler = this;  // For debugging purposes
    }

    async request(method, url, data = {}) {
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();
            xhr.open(method, url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(JSON.parse(xhr.responseText));
                } else {
                    reject({
                        status: xhr.status,
                        statusText: xhr.statusText,
                        body: JSON.parse(xhr.responseText)
                    });
                }
            };
            xhr.onerror = () => {
                reject({
                    status: xhr.status,
                    statusText: xhr.statusText,
                    body: xhr.responseText
                });
            };
            xhr.send(JSON.stringify(data));
        });
    }

    async get_accounts() {
        let response = await fetch(`${this._base}/api/v1/spotifyd/accounts`);

        if (response.ok) {
            let json = await response.json();
            console.log('GET /api/v1/spotifyd/accounts:', json)
            return json
        } else {
            console.log(`HTTP error: ${response.status}`);
        }
    }

    async add_account(data) {
        return await this.request(
            'POST',
            `${this._base}/api/v1/spotifyd/accounts`,
            data
        );

    }

    async edit_account(id, data) {
        return await this.request(
            'PUT',
            `${this._base}/api/v1/spotifyd/accounts/${id}`,
            data
        );
    }

    async remove_account(id) {
        return await this.request(
            'DELETE',
            `${this._base}/api/v1/spotifyd/accounts/${id}`
        );
    }
}
