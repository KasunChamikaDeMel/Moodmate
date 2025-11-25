const { app, BrowserWindow, screen, ipcMain, Tray, Menu } = require('electron');
const path = require('path');
const http = require('http');

app.commandLine.appendSwitch('force-device-scale-factor', '1');

let petWindow, settingsWindow, chatWindow, tray, dragInterval;
let hideTimeout = null; // timer

// --- 1. SERVER (Timer Logic gets here) ---
const server = http.createServer((req, res) => {
    console.log(`📥 Received ${req.method} request to ${req.url}`);
    
    if (req.method === 'POST' && req.url === '/trigger') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                console.log(`📨 Received emotion trigger:`, data);

                if (!petWindow) {
                    console.log("⚠️ Pet window not created yet, creating now...");
                    // Wait for app to be ready before creating window
                    if (app.isReady()) {
                        createPetWindow();
                        // Wait a moment for window to be ready
                        setTimeout(() => {
                            if (petWindow && !petWindow.isDestroyed()) {
                                petWindow.show();
                                petWindow.restore();
                                petWindow.focus();
                                petWindow.webContents.send('backend-trigger', data);
                                console.log(`🐾 Pet window created and shown with emotion: ${data.emotion || 'unknown'}`);
                            }
                        }, 500);
                    } else {
                        console.log("⚠️ App not ready yet, will create window when ready");
                        app.whenReady().then(() => {
                            createPetWindow();
                            setTimeout(() => {
                                if (petWindow && !petWindow.isDestroyed()) {
                                    petWindow.show();
                                    petWindow.restore();
                                    petWindow.focus();
                                    petWindow.webContents.send('backend-trigger', data);
                                    console.log(`🐾 Pet window created and shown with emotion: ${data.emotion || 'unknown'}`);
                                }
                            }, 500);
                        });
                    }
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'Triggered', emotion: data.emotion, note: 'Window being created' }));
                    return;
                }

                if (petWindow && !petWindow.isDestroyed()) {
                    // 1. show pet (Don't auto-hide - user will hide it manually)
                    petWindow.show();
                    petWindow.restore();
                    petWindow.focus();  // Bring window to front
                    petWindow.webContents.send('backend-trigger', data);

                    // 2. Clear any old hide timeout (no longer auto-hiding pet window)
                    if (hideTimeout) clearTimeout(hideTimeout);
                    hideTimeout = null;  // Pet stays visible until user hides it
                    
                    console.log(`🐾 Pet window shown with emotion: ${data.emotion || 'unknown'}`);
                } else {
                    console.log("❌ Pet window is destroyed or not available");
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'Triggered', emotion: data.emotion }));
            } catch (e) {
                console.error("❌ Error processing trigger:", e);
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid request' }));
            }
        });
    } else {
        // Handle other requests (like GET for health check)
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'Pet server running', port: actualPort }));
    }
});
// Store the actual port being used
let actualPort = 4000;

// Try to listen on port 4000, if it fails try alternative ports
const tryListen = (port, maxAttempts = 5) => {
    if (port > 4000 + maxAttempts) {
        console.error('❌ Could not find available port for pet server');
        return;
    }
    
    server.once('error', (err) => {
        if (err.code === 'EADDRINUSE') {
            console.log(`⚠️ Port ${port} is in use, trying ${port + 1}...`);
            tryListen(port + 1, maxAttempts);
        } else {
            console.error(`❌ Error starting pet server: ${err.message}`);
        }
    });
    
    server.listen(port, '127.0.0.1', () => {
        actualPort = port;
        console.log(`🐶 Pet listening on Port ${port}`);
        console.log(`📡 Pet trigger endpoint: http://localhost:${port}/trigger`);
    });
};

tryListen(4000);

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

// (Settings & Chat Windows)
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

// Stop Timer Logic when user clicks/interacts
ipcMain.on('stop-timer', () => {
    if (hideTimeout) {
        console.log("🛑 User Clicked! Timer Stopped.");
        clearTimeout(hideTimeout);
        hideTimeout = null; // Now the pet stays visible
    }
});

// Drag Logic (Size Lock)
ipcMain.on('drag-start', (event, cursorOffset) => {
    clearInterval(dragInterval);
    const currentSize = petWindow.getSize();
    
    // stop Timer when dragging starts
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

// Mouse Ignore & Settings Logic
ipcMain.on('set-ignore-mouse', (e, ignore) => {
    const win = BrowserWindow.fromWebContents(e.sender);
    win.setIgnoreMouseEvents(ignore, { forward: true });
});

ipcMain.on('update-settings', (event, data) => {
    if (data.type === 'size') {
        const s = parseInt(data.value);
        petWindow.setBounds({ width: s, height: s + 150 });
    }
    petWindow.webContents.send('apply-setting', data);
});

ipcMain.on('open-settings', () => settingsWindow.show());
ipcMain.on('show-context-menu', () => {
    // Right Click ,then stop Timer
    if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null; }
    const menu = Menu.buildFromTemplate([
        { label: '💬 Live Chat', click: () => chatWindow.show() },
        { label: '⚙️ Settings', click: () => settingsWindow.show() },
        { label: '❌ Hide Pet', click: () => petWindow.hide() }
    ]);
    menu.popup(petWindow);
});

// --- 🔌 SYSTEM MONITORING (MoodMate Senses) ---

// --- 🔌 SYSTEM MONITORING (Power Fix) ---
const si = require('systeminformation');
const dns = require('dns'); 

let lastState = { charging: false, internet: true };

setInterval(async () => {
    if (!petWindow || petWindow.isDestroyed()) return;

    try {
        // 1. BATTERY & CHARGING CHECK
        const battery = await si.battery();
        const isPluggedIn = battery.acConnected || battery.isCharging;

        // A.(Plugged In)
        if (isPluggedIn && !lastState.charging) {
            console.log("🔌 Detected: Power Connected");
            petWindow.webContents.send('backend-trigger', {
                emotion: 'poweron',
                message: "Yum! Electricity! Thanks for the power! ⚡"
            });
            lastState.charging = true;
            return;
        }

        // B.(Unplugged)
        if (!isPluggedIn && lastState.charging) {
            console.log("🔌 Detected: Power Removed");
            lastState.charging = false;
            petWindow.webContents.send('backend-trigger', {
                emotion: 'poweroff',
                message: "Oh no! Charger removed! I'm losing power... 🔌❌"
            });
            return;
        }

        // C.(Low Battery - Laptop only)
        // If battery below 20% and not charging
        if (battery.hasBattery && !isPluggedIn && battery.percent < 20) {
             petWindow.webContents.send('backend-trigger', {
                emotion: 'stress',
                message: `🔋 I'm weak... Battery is at ${battery.percent}%!`
            });
            return;
        }

        // 2. INTERNET CHECK
        dns.lookup('google.com', (err) => {
            if (err && lastState.internet) {
                petWindow.webContents.send('backend-trigger', {
                    emotion: 'wifioff',
                    message: "Oh no! No Internet! I feel lonely... 🌍❌"
                });
                lastState.internet = false;
            } else if (!err && !lastState.internet) {
                petWindow.webContents.send('backend-trigger', {
                    emotion: 'wifion',
                    message: "Yay! We are back online! 🌐✨"
                });
                lastState.internet = true;
            }
        });

    } catch (error) {
        console.error("System Check Error:", error);
    }

}, 5000);