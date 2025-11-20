const { app, BrowserWindow, screen, ipcMain, Tray, Menu } = require('electron');
const path = require('path');
const http = require('http');

app.commandLine.appendSwitch('force-device-scale-factor', '1');

let petWindow, settingsWindow, chatWindow, tray, dragInterval;
let hideTimeout = null; // ⏳ මේක තමයි අලුත් Timer එක (Main එකේ තියෙන්නේ)

// --- 1. SERVER (Timer Logic එක මෙතනට ගත්තා) ---
const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/trigger') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);

                if (petWindow) {
                    // 1. පූසාව පෙන්නන්න
                    petWindow.show();
                    petWindow.restore();
                    petWindow.webContents.send('backend-trigger', data);

                    // 2. පරණ Timer තිබ්බොත් මකන්න
                    if (hideTimeout) clearTimeout(hideTimeout);

                    // 3. අලුත් Timer එක දාන්න (තත්පර 10කින් හැංගෙන්න)
                    console.log("⏳ Timer Started: 10 Seconds...");
                    hideTimeout = setTimeout(() => {
                        console.log("👻 Time's up! Hiding Pet.");
                        petWindow.hide();
                    }, 10000);
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'Triggered' }));
            } catch (e) {
                res.writeHead(400); res.end('Error');
            }
        });
    }
});
server.listen(4000, () => console.log('🐶 Pet listening on Port 4000'));

// --- 2. WINDOWS CREATION ---
function createPetWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    petWindow = new BrowserWindow({
        width: 300, height: 450,
        x: width - 350, y: height - 500,
        transparent: true, frame: false, alwaysOnTop: true, skipTaskbar: true, resizable: true,
        show: false,
        webPreferences: { nodeIntegration: true, contextIsolation: false }
    });
    petWindow.loadFile('index.html');
    petWindow.setIgnoreMouseEvents(true, { forward: true });
}

// (Settings & Chat Windows - පරණ විදිහමයි)
function createSettingsWindow() {
    settingsWindow = new BrowserWindow({ width: 300, height: 400, show: false, frame: true, autoHideMenuBar: true, webPreferences: { nodeIntegration: true, contextIsolation: false } });
    settingsWindow.loadFile('settings.html');
    settingsWindow.on('close', (e) => { e.preventDefault(); settingsWindow.hide(); });
}

function createChatWindow() {
    chatWindow = new BrowserWindow({ width: 350, height: 500, show: false, frame: true, autoHideMenuBar: true, webPreferences: { nodeIntegration: true, contextIsolation: false } });
    chatWindow.loadFile('chat.html');
    chatWindow.on('close', (e) => { e.preventDefault(); chatWindow.hide(); });
}

function createTray() {
    tray = new Tray(path.join(__dirname, 'assets', 'icon.png'));
    const contextMenu = Menu.buildFromTemplate([
        { label: 'Show Pet', click: () => petWindow.show() },
        { label: 'Live Chat', click: () => chatWindow.show() },
        { label: 'Settings', click: () => settingsWindow.show() },
        { label: 'Quit', click: () => app.exit() }
    ]);
    tray.setContextMenu(contextMenu);
}

app.whenReady().then(() => {
    createPetWindow();
    createSettingsWindow();
    createChatWindow();
    createTray();
});

// --- 3. SYSTEM LOGIC ---

// User පූසාව Click කළාම Timer එක නවත්තන්න ඕනේ
ipcMain.on('stop-timer', () => {
    if (hideTimeout) {
        console.log("🛑 User Clicked! Timer Stopped.");
        clearTimeout(hideTimeout);
        hideTimeout = null; // දැන් පූසා දිගටම ඉන්නවා
    }
});

// Drag Logic (Size Lock)
ipcMain.on('drag-start', (event, cursorOffset) => {
    clearInterval(dragInterval);
    const currentSize = petWindow.getSize();
    
    // Drag කරනකොටත් Timer එක නවත්තන්න ඕනේ
    if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null; }

    dragInterval = setInterval(() => {
        const cursorPoint = screen.getCursorScreenPoint();
        petWindow.setBounds({
            x: cursorPoint.x - cursorOffset.x, y: cursorPoint.y - cursorOffset.y,
            width: currentSize[0], height: currentSize[1]
        });
    }, 10);
});

ipcMain.on('drag-end', () => clearInterval(dragInterval));

// Mouse Ignore & Settings Logic (පරණ ඒවා)
ipcMain.on('set-ignore-mouse', (e, ignore) => {
    const win = BrowserWindow.fromWebContents(e.sender);
    win.setIgnoreMouseEvents(ignore, { forward: true });
});

ipcMain.on('update-settings', (event, data) => {
    if (data.type === 'size') {
        const s = parseInt(data.value);
        petWindow.setBounds({ width: s, height: s + 150 });
        // const b = petWindow.getBounds();
        // petWindow.setBounds({ x: b.x, y: b.y, width: s, height: s });
    }
    petWindow.webContents.send('apply-setting', data);
});

ipcMain.on('open-settings', () => settingsWindow.show());
ipcMain.on('show-context-menu', () => {
    // Right Click කළත් Timer එක නවත්තමු
    if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null; }
    const menu = Menu.buildFromTemplate([
        { label: '💬 Live Chat', click: () => chatWindow.show() },
        { label: '⚙️ Settings', click: () => settingsWindow.show() },
        { label: '❌ Hide Pet', click: () => petWindow.hide() }
    ]);
    menu.popup(petWindow);
});