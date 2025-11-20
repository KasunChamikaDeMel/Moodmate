const { ipcMain, Tray, Menu, app } = require('electron');
const path = require('path');
const PetWindow = require('./PetWindow');
const SettingsWindow = require('./SettingsWindow');

class AppController {
    constructor() {
        this.petWindow = new PetWindow();
        this.settingsWindow = new SettingsWindow();
        this.tray = null;
        
        this.initTray();
        this.handleIPC();
    }

    initTray() {
        const iconPath = path.join(__dirname, '../assets/icon.png');
        this.tray = new Tray(iconPath);
        
        const contextMenu = Menu.buildFromTemplate([
            { label: 'Settings', click: () => this.settingsWindow.show() },
            { type: 'separator' },
            { label: 'Quit', click: () => { app.exit(); } }
        ]);
        
        this.tray.setToolTip('MoodMate');
        this.tray.setContextMenu(contextMenu);
    }

handleIPC() {
        // 1. Mouse Logic (Click Through)
        ipcMain.on('set-ignore-mouse', (event, shouldIgnore) => {
            this.petWindow.setClickable(!shouldIgnore);
        });

        // 2. Settings Updates
        ipcMain.on('update-settings', (event, data) => {
            this.petWindow.webContents.send('apply-setting', data);
            if (data.type === 'size') {
                this.petWindow.resizePet(data.value);
            }
        });

        // 3. Open Settings
        ipcMain.on('open-settings', () => {
            this.settingsWindow.show();
        });

        // --- 4. DRAG LOGIC (අලුත් ක්‍රමය - Bulletproof) ---
        let dragInterval = null;

        ipcMain.on('drag-start', (event, clickOffset) => {
            const { screen } = require('electron');
            
            // පරණ Interval එකක් තිබ්බොත් අයින් කරන්න
            if (dragInterval) clearInterval(dragInterval);

            // තත්පරේට 60 සැරයක් Mouse එක තියෙන තැන බලන්න
            dragInterval = setInterval(() => {
                const cursor = screen.getCursorScreenPoint();
                // Mouse එක තියෙන තැනින්, අල්ලපු තැන (Offset) අඩු කරලා Window එක තියන්න
                this.petWindow.setPosition(cursor.x - clickOffset.x, cursor.y - clickOffset.y);
            }, 1000 / 60); // 60 FPS Smoothness
        });

        ipcMain.on('drag-end', () => {
            if (dragInterval) {
                clearInterval(dragInterval); // Drag කිරීම නවත්තන්න
                dragInterval = null;
            }
        });
    }
}

module.exports = AppController;