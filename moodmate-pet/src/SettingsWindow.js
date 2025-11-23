const { BrowserWindow } = require('electron');

class SettingsWindow extends BrowserWindow {
    constructor() {
        super({
            width: 300,
            height: 400,
            show: false, 
            frame: true, 
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            }
        });

        this.loadFile('settings.html');

        // Close to tray instead of quitting
        this.on('close', (e) => {
            e.preventDefault();
            this.hide();
        });
    }

    toggle() {
        if (this.isVisible()) {
            this.hide();
        } else {
            this.show();
        }
    }
}

module.exports = SettingsWindow;