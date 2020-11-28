import ApiHandler from "./api.js";
import AppUI from "./ui.js";

// function RequestException(status_code, response) {
//     this.detail = response.detail;
//     this.name = 'Request exception';
//     this.status_code = status_code;
//     // this.toString = () => {
//     //     return this.name + this.detail;
//     // }
// }
//
// RequestException.prototype = Object.create(Error.prototype);
// RequestException.prototype.constructor = RequestException;

async function init() {
    let api = new ApiHandler();
    let ui = new AppUI();

    let accounts = await api.get_accounts();
    if (accounts) {
        for (const acc of Object.values(accounts.items)) {
            await ui.append_item(acc);
        }
    } else {
        // TODO: Handle an empty list
        console.log(accounts);
    }
}

window.onload = () => {
    init().then();
}
