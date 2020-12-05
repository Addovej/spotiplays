export default class ApiHandler {
    constructor() {
        /** @type {string} */
        this._base = '';
        window.ApiHandler = this;  // For debugging purposes
    }

    /**
     * @param {string} method
     * @param {string} url
     * @param {Object} data
     * @return {Promise}
     */
    async #_request(method, url, data = {}) {
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

    /**
     * @return {Object}
     */
    async get_current() {
        return await this.#_request(
            'GET',
            `${this._base}/api/v1/spotifyd/current`
        )
    }

    /**
     * @param {number} id
     * @return {Object}
     */
    async set_current(id) {
        return await this.#_request(
            'POST',
            `${this._base}/api/v1/spotifyd/switch/${id}`
        )
    }

    /**
     * @return {Object}
     */
    async get_accounts() {
        return await this.#_request(
            'GET',
            `${this._base}/api/v1/spotifyd/accounts`
        )
    }

    /**
     * @param {Object} data
     * @return {Object}
     */
    async add_account(data) {
        return await this.#_request(
            'POST',
            `${this._base}/api/v1/spotifyd/accounts`,
            data
        );

    }

    /**
     * @param {number} id
     * @param {Object} data
     * @return {Object}
     */
    async edit_account(id, data) {
        return await this.#_request(
            'PUT',
            `${this._base}/api/v1/spotifyd/accounts/${id}`,
            data
        );
    }

    /**
     * @param {number} id
     * @return {Object}
     */
    async remove_account(id) {
        return await this.#_request(
            'DELETE',
            `${this._base}/api/v1/spotifyd/accounts/${id}`
        );
    }
}
