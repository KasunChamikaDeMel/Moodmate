const { BrowserWindow } = require('electron');

class PetWindow extends BrowserWindow {
    constructor() {
        super({
            width: 300,
            height: 300,
            transparent: true,
            frame: false,
            alwaysOnTop: true,
            skipTaskbar: true,
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            }
        });

        // load pet
        this.loadFile('index.html');

        // initialize as click-through
        this.setIgnoreMouseEvents(true, { forward: true });
    }

    // resize pet method
    resizePet(size) {
        this.setSize(parseInt(size), parseInt(size));
    }

    // mouse control method
    setClickable(isClickable) {
        if (isClickable) {
            this.setIgnoreMouseEvents(false);
        } else {
            this.setIgnoreMouseEvents(true, { forward: true });
        }
    }
}

module.exports = PetWindow;