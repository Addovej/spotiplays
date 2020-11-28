import ApiHandler from './api.js';

const api = new ApiHandler();


class ListEvent extends EventTarget {
    set_item(acc) {
        this.dispatchEvent(new MessageEvent('set_item', {data: acc}));
    }

    change_item(acc) {
        this.dispatchEvent(new MessageEvent('change_item', {data: acc}));
    }

    remove_item(id) {
        this.dispatchEvent(new MessageEvent('remove_item', {data: id}));
    }
}

const list_event = new ListEvent();


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
            let accounts = await api.get_accounts();
            if (accounts.items.length !== 0) {
                for (const acc of Object.values(accounts.items)) {
                    await this.append_item(acc);
                }
            } else {
                let empty = document.querySelector('body .empty');
                empty.innerHTML = '<p>There not any accounts</p>';
            }
        } catch (e) {
            console.log('Error with init_data: ', e)
        }
    }

    async create_item_list(acc) {
        let label = document.createElement('label');
        label.innerText = `${acc.name} (${acc.username})`;

        let remove_btn = document.createElement('span');
        remove_btn.className = 'remove';
        remove_btn.appendChild(document.createTextNode('\u2715'));
        remove_btn.onclick = () => {
            this.remove_item(acc);
        };

        let edit_btn = document.createElement('span');
        edit_btn.className = 'edit';
        edit_btn.appendChild(document.createTextNode('\u2630'));  // Or '\u270E'
        edit_btn.onclick = () => {
            this.edit_item(acc);
        };

        let item = document.createElement('li');
        item.id = `account-item-${acc.id}`;
        item.appendChild(label);
        item.appendChild(edit_btn);
        item.appendChild(remove_btn);

        return item;
    }

    async append_item(acc) {
        this.list.appendChild(await this.create_item_list(acc));
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

    async remove_item(acc) {
        this.remove.title.innerText = `Remove '${acc.name}' (login=${acc.username}) account?`;
        this.remove.buttons.confirm.onclick = () => {
            this.#_remove_confirmed(acc.id);
        };
        this.#_open_remove();
    }

    // Handle actions API calls

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
            this.append_item(event.data).then();
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

function get_list_accounts() {
    return document.getElementById('accounts');
}

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