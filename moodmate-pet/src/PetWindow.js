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

        // පූසාව Load කරනවා
        this.loadFile('index.html');

        // මුලින්ම Ghost Mode (අල්ලන්න බෑ)
        this.setIgnoreMouseEvents(true, { forward: true });
    }

    // පූසාගේ Size එක වෙනස් කරන Method එක
    resizePet(size) {
        this.setSize(parseInt(size), parseInt(size));
    }

    // මවුස් එක පාලනය කරන Method එක
    setClickable(isClickable) {
        if (isClickable) {
            this.setIgnoreMouseEvents(false);
        } else {
            this.setIgnoreMouseEvents(true, { forward: true });
        }
    }
}

module.exports = PetWindow;