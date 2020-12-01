import ApiHandler from './api.js';

const api = new ApiHandler();


class ListEvent extends EventTarget {

    /** @param {Object} acc */
    set_item(acc) {
        this.dispatchEvent(new MessageEvent('set_item', {data: acc}));
    }

    /** @param {Object} acc */
    change_item(acc) {
        this.dispatchEvent(new MessageEvent('change_item', {data: acc}));
    }

    /** @param {number} id */
    remove_item(id) {
        this.dispatchEvent(new MessageEvent('remove_item', {data: id}));
    }
}

const list_event = new ListEvent();


class AccountModel {
    /**
     * Account object
     * @type Object
     */
    constructor(acc) {
        /** @type number */
        this.id = acc.id;

        /** @type string */
        this.name = acc.name;

        /** @type string */
        this.username = acc.username;

        /** @type Object */
        this.credentials_verification = acc.credentials_verification;
    }

    /** @type boolean */
    get is_verified() {
        return this.credentials_verification.state === 'OK';
    }
}


export default class AppUI {
    constructor() {
        window.AppUI = AppUI;

        // Accounts list
        this.list = get_list_accounts();

        // Modals for managing
        this.create = get_create_modal();
        this.edit = get_edit_modal();
        this.remove = get_remove_modal();

        this.#_initialize_clicks();
        this.#_initialize_events();
    }

    async init_data() {
        try {
            const current_active = await api.get_current();
            let accounts = await api.get_accounts();
            if (accounts.items.length !== 0) {
                for (const acc of Object.values(accounts.items)) {
                    await this.append_item(
                        new AccountModel(acc),
                        current_active?.id === acc.id
                    );
                }
            } else {
                let empty = document.querySelector('body .empty');
                empty.innerHTML = '<p>There not any accounts</p>';
            }
        } catch (e) {
            console.log('Error with init_data: ', e)
        }
    }

    /**
     * @param {AccountModel} acc
     * @param {boolean} is_current
     *
     * @return {HTMLElement}
     */
    async create_item_list(acc, is_current) {
        console.log(acc)
        const choose = is_current ? 'chosen' : 'choose';
        const li_content = `
            <label>${acc.name} (${acc.username})</label>
            <div>
                <span class="${choose} main-btn">\u2713</span>
                <span class="edit main-btn">\u2630</span>  <!-- Or \u270E -->
                <span class="remove main-btn">\u2715</span>
            </div>
        `;

        let item = document.createElement('li');
        item.id = `account-item-${acc.id}`;
        item.innerHTML = li_content;
        item.querySelector(`.${choose}`).onclick = () => {
            this.switch_account(acc);
        };
        item.querySelector('.edit').onclick = () => {
            this.edit_item(acc);
        };
        item.querySelector('.remove').onclick = () => {
            this.remove_item(acc);
        };
        if (is_current) {
            item.className = 'account-item-active';
        }
        if (!acc.is_verified) {
            item.className = 'account-item-verification-failed';
            item.title = acc.credentials_verification.details;
        }

        return item;
    }

    /**
     * @param {AccountModel} acc
     * @param {boolean} is_current
     */
    async append_item(acc, is_current) {
        this.list.appendChild(await this.create_item_list(acc, is_current));
    }

    /** @param {AccountModel} acc */
    async switch_account(acc) {
        try {
            let li = this.list.querySelector(`#account-item-${acc.id}`);
            if (li.className !== 'account-item-active' && acc.is_verified) {
                console.log('Switch account: ', acc);
                await api.set_current(acc.id);

                this.list.querySelector('.account-item-active').className = '';
                this.list.querySelector('.chosen').className = 'choose';

                li.className = 'account-item-active';
                li.querySelector('.choose').className = 'chosen';
            }
        } catch (e) {
            console.log('Error with switching account', e);
        }
    }

    async create_item() {
        this.create.buttons.save.onclick = () => {
            this.#_create_saved(
                this.create.inputs.name,
                this.create.inputs.username,
                this.create.inputs.password
            );
        }
        this.#_open_create();
    }

    /** @param {AccountModel} acc */
    async edit_item(acc) {
        this.edit.title.innerHTML = `Editing '${acc.name}' (login=${acc.username}) account.`;

        this.edit.inputs.name.value = acc.name;
        this.edit.inputs.username.value = acc.username;

        this.edit.buttons.save.onclick = () => {
            this.#_edit_saved(
                acc,
                this.edit.inputs.name,
                this.edit.inputs.username,
                this.edit.inputs.password
            );
        }
        this.#_open_edit();
    }

    /** @param {AccountModel} acc */
    async remove_item(acc) {
        this.remove.title.innerText = `Remove '${acc.name}' (login=${acc.username}) account?`;
        this.remove.buttons.confirm.onclick = () => {
            this.#_remove_confirmed(acc.id);
        };
        this.#_open_remove();
    }

    // Handle actions API calls

    /**
     * @param {Object} name
     * @param {Object} username
     * @param {Object} password
     */
    async #_create_saved(name, username, password) {
        if (!name.value || !username.value || !password.value) {
            alert('All fields are required');
        } else {
            let data = {
                name: name.value,
                username: username.value,
                password: password.value
            }
            console.log('Data to send: ', data);
            try {
                let res = await api.add_account(data);
                const acc = {
                    id: res.id,
                    name: data.name,
                    username: data.username
                }
                list_event.set_item(acc);
                this.#_close_create();
            } catch (e) {
                console.log('Error with account creation', e);
            }
        }
    }

    /**
     * @param {AccountModel} acc
     * @param {Object} name
     * @param {Object} username
     * @param {Object} password
     */
    async #_edit_saved(acc, name, username, password) {
        let data = {}

        if (name.value !== acc.name) {
            data.name = name.value;
        }
        if (username.value !== acc.username) {
            data.username = username.value;
        }
        if (password.value) {
            data.password = password.value;
        }

        if (Object.keys(data).length !== 0) {
            console.log('Data to send: ', data);
            try {
                let res = await api.edit_account(acc.id, data);
                console.log('Response[_edit_saved]: ', res);
                list_event.change_item({
                    id: acc.id,
                    name: name.value,
                    username: username.value
                })
                this.#_close_edit();
            } catch (e) {
                console.log('Error with account editing', e);
            }
        } else {
            console.log('Nothing to send');
        }
    }

    /** @param {number} id */
    async #_remove_confirmed(id) {
        try {
            await api.remove_account(id);
            console.log('remove item in _remove_confirmed');
            list_event.remove_item(id);
            this.#_close_remove();
        } catch (e) {
            console.log('Error with account removing', e);
        }
    }

    #_initialize_events() {
        list_event.addEventListener('set_item', (event) => {
            console.log(event.type, event.data);
            this.append_item(new AccountModel(event.data), false).then();
        });

        list_event.addEventListener('change_item', (event) => {
            console.log(event.type, event.data);
            document.querySelector(
                `#account-item-${event.data.id} label`
            ).innerText = `${event.data.name} (${event.data.username})`;
        });

        list_event.addEventListener('remove_item', (event) => {
            console.log(event.type, event.data);
            this.list.removeChild(
                document.getElementById(`account-item-${event.data}`)
            );
        });
    }

    #_initialize_clicks() {
        // Buttons bindings
        this.create.buttons.close.onclick = () => {
            this.#_close_create();
        };
        this.create.buttons.cancel.onclick = () => {
            this.#_close_create();
        };
        this.create.add.onclick = () => {
            this.create_item().then();
        };

        this.edit.buttons.close.onclick = () => {
            this.#_close_edit();
        };
        this.edit.buttons.cancel.onclick = () => {
            this.#_close_edit();
        };

        this.remove.buttons.close.onclick = () => {
            this.#_close_remove();
        };
        this.remove.buttons.cancel.onclick = () => {
            this.#_close_remove();
        };

        // Click anywhere to close modal handler
        window.onclick = (event) => {
            if (event.target === this.create.modal) {
                this.#_close_create();
            } else if (event.target === this.edit.modal) {
                this.#_close_edit();
            } else if (event.target === this.remove.modal) {
                this.#_close_remove();
            }
        }

        // Close all modals on Escape
        document.onkeyup = (e) => {
            if (e.key === 'Escape') {
                this.#_close_create();
                this.#_close_edit();
                this.#_close_remove();
            }
        }
    }

    // Methods for binding open-close modal

    #_close_create() {
        this.create.modal.style.display = 'none';
        Object.values(this.create.inputs).forEach((input) => {
            input.value = null;
        });
    }

    #_open_create() {
        this.create.modal.style.display = 'block';
    }

    #_close_edit() {
        this.edit.modal.style.display = 'none';
        Object.values(this.edit.inputs).forEach((input) => {
            input.value = null;
        });
    }

    #_open_edit() {
        this.edit.modal.style.display = 'block';
    }

    #_close_remove() {
        this.remove.modal.style.display = 'none';
    }

    #_open_remove() {
        this.remove.modal.style.display = 'block';
    }
}

// Components getters

/** @return {HTMLElement} */
function get_list_accounts() {
    return document.getElementById('accounts');
}

/** @return {Object} */
function get_create_modal() {
    return {
        modal: document.getElementById('create-account'),
        add: document.getElementById('add-new-account'),
        buttons: {
            cancel: document.getElementById('create-cancel'),
            close: document.getElementById('create-close'),
            save: document.getElementById('create-save')
        },
        inputs: {
            name: document.getElementById('create-name'),
            username: document.getElementById('create-username'),
            password: document.getElementById('create-password')
        }
    }
}

/** @return {Object} */
function get_edit_modal() {
    return {
        modal: document.getElementById('edit-account'),
        title: document.getElementById('edit-title'),
        buttons: {
            cancel: document.getElementById('edit-cancel'),
            close: document.getElementById('edit-close'),
            save: document.getElementById('edit-save')
        },
        inputs: {
            name: document.getElementById('edit-name'),
            username: document.getElementById('edit-username'),
            password: document.getElementById('edit-password')
        }
    }
}

/** @return {Object} */
function get_remove_modal() {
    return {
        modal: document.getElementById('remove-account'),
        title: document.getElementById('remove-title'),
        buttons: {
            confirm: document.getElementById('remove-confirm'),
            cancel: document.getElementById('remove-cancel'),
            close: document.getElementById('remove-close')
        },
    }
}
