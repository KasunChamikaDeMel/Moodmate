const { BrowserWindow } = require('electron');

class SettingsWindow extends BrowserWindow {
    constructor() {
        super({
            width: 300,
            height: 400,
            show: false, // මුලින් හංගලා තියන්න
            frame: true, // මේකට බෝඩර් එකක් ඕනේ
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            }
        });

        this.loadFile('settings.html');

        // Close කළාම කෙලින්ම අයින් නොවී හැංගෙන්න හදමු
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